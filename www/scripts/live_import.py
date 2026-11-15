"""Import the cards of the historical live site (edrefcard.info).

The live site stored every card as configs/<id[:2]>/<id>.binds plus a pickled
<id>.replay (saveReplayInfo in the upstream bindings.py): a dict holding the
title, styling, display groups, timestamp, devices and warnings.

This module copies the .binds sources into our configs folder and recreates
the database rows with the original id, title, styling, display groups and
date, so every /binds/<id> link shared on the forums keeps working. Devices
and warnings are recomputed from the .binds with the current parser, which
knows more controllers than the live one did.

Nothing already present is overwritten: an id that exists here (database row
or .binds file) is skipped and reported, as "duplicate" when the source is
byte-identical and "clash" otherwise.
"""
import datetime
import os
import pickle
from dataclasses import dataclass, field
from pathlib import Path

from . import database
from .models import Config, Errors
from .parser import parseBindings

STYLINGS = {'None', 'Group', 'Category', 'Modifier'}

# What the live replay mode used when a .replay had no displayGroups key.
LIVE_DEFAULT_GROUPS = ['Galaxy map', 'General', 'Head look', 'SRV', 'Ship', 'UI']

MAX_BINDS_BYTES = 5 * 1024 * 1024

# The only globals a live .replay needs: the timestamp is a timezone-aware
# datetime, everything else is built from dicts, lists and strings.
_ALLOWED_GLOBALS = {
    ('datetime', 'datetime'),
    ('datetime', 'date'),
    ('datetime', 'timedelta'),
    ('datetime', 'timezone'),
    ('collections', 'OrderedDict'),
    ('builtins', 'set'),
    ('builtins', 'frozenset'),
}


class ReplayError(Exception):
    """A .replay file that cannot be read safely."""


class _RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in _ALLOWED_GLOBALS:
            return super().find_class(module, name)
        raise ReplayError(f'forbidden global {module}.{name}')


def load_replay(path):
    """Read a live .replay without letting it run code (pickle.load would)."""
    try:
        with Path(path).open('rb') as handle:
            data = _RestrictedUnpickler(handle).load()
    except ReplayError:
        raise
    except Exception as exc:  # truncated or corrupt file
        raise ReplayError(f'unreadable: {exc}') from exc
    if not isinstance(data, dict):
        raise ReplayError(f'expected a dict, got {type(data).__name__}')
    return data


def replay_metadata(data):
    """Normalise a live replay dict into create_configuration arguments."""
    description = data.get('description')
    description = '' if description is None else str(description).strip()

    styling = str(data.get('styling') or 'None')
    if styling not in STYLINGS:
        styling = 'None'

    groups = data.get('displayGroups')
    if groups is None:
        groups = LIVE_DEFAULT_GROUPS
    groups = [g for g in groups if isinstance(g, str)]

    created_at = data.get('timestamp')
    if isinstance(created_at, datetime.datetime):
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=datetime.UTC)
        # Stored as text in the format sqlite's datetime adapter wrote for
        # the other rows (that adapter is deprecated since Python 3.12).
        created_at = created_at.astimezone(datetime.UTC).isoformat(' ')
    else:
        created_at = None

    return {
        'description': description,
        'styling': styling,
        'display_groups': groups,
        'created_at': created_at,
    }


@dataclass
class ImportReport:
    """Outcome of one run; every id lands in exactly one list."""
    dry_run: bool = False
    imported: list = field(default_factory=list)
    duplicates: list = field(default_factory=list)
    clashes: list = field(default_factory=list)
    missing_binds: list = field(default_factory=list)
    orphan_binds: list = field(default_factory=list)
    invalid_ids: list = field(default_factory=list)
    bad_replays: list = field(default_factory=list)
    parse_errors: list = field(default_factory=list)
    duplicate_sources: list = field(default_factory=list)

    def counts(self):
        return {name: len(value) for name, value in self.__dict__.items()
                if isinstance(value, list)}

    def as_dict(self):
        result = {'dry_run': self.dry_run, 'counts': self.counts()}
        result.update({name: value for name, value in self.__dict__.items()
                       if isinstance(value, list)})
        return result


def _index(source_dir, suffix, report):
    """Map id -> path for every file with this suffix under source_dir."""
    found = {}
    for path in sorted(Path(source_dir).rglob(f'*{suffix}')):
        if not path.is_file():
            continue
        config_id = path.stem
        if config_id in found:
            report.duplicate_sources.append({'id': config_id, 'path': str(path)})
            continue
        found[config_id] = path
    return found


def _chown_like(path, reference):
    """Give a file written by root (docker exec) to the configs folder owner."""
    if not hasattr(os, 'geteuid') or os.geteuid() != 0:
        return
    stat = reference.stat()
    os.chown(path, stat.st_uid, stat.st_gid)


def import_live_configs(source_dir, dry_run=False, limit=None, log=None):
    """Import every <id>.replay + <id>.binds pair found under source_dir.

    Returns an ImportReport. With dry_run, nothing is written but every
    check (replay, parser, collisions) still runs.
    """
    report = ImportReport(dry_run=dry_run)
    replays = _index(source_dir, '.replay', report)
    binds = _index(source_dir, '.binds', report)
    report.orphan_binds = sorted(set(binds) - set(replays))
    known_ids = set(database.get_all_config_ids())
    configs_root = Config.configsPath()

    processed = 0
    for config_id in sorted(replays):
        if limit is not None and processed >= limit:
            break
        processed += 1
        if log and processed % 250 == 0:
            log(f'{processed}/{len(replays)}...')

        if not Config.isValidName(config_id):
            report.invalid_ids.append(config_id)
            continue
        source = binds.get(config_id)
        if source is None:
            report.missing_binds.append(config_id)
            continue
        try:
            meta = replay_metadata(load_replay(replays[config_id]))
        except ReplayError as exc:
            report.bad_replays.append({'id': config_id, 'error': str(exc)})
            continue

        raw = source.read_bytes()
        if len(raw) > MAX_BINDS_BYTES:
            report.parse_errors.append({'id': config_id, 'error': 'file too large'})
            continue
        target = Config(config_id).pathWithSuffix('.binds')
        if config_id in known_ids or target.exists():
            same = target.exists() and target.read_bytes() == raw
            (report.duplicates if same else report.clashes).append(config_id)
            continue

        try:
            xml = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            report.parse_errors.append({'id': config_id, 'error': 'not UTF-8'})
            continue
        errors = Errors()
        try:
            (_keys, _modifiers, devices) = parseBindings(
                config_id, xml, meta['display_groups'], errors)
        except Exception as exc:
            report.parse_errors.append({'id': config_id, 'error': str(exc)})
            continue
        if errors.errors:
            report.parse_errors.append({'id': config_id, 'error': str(errors.errors)})
            continue

        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            _chown_like(target, configs_root)
            _chown_like(target.parent, configs_root)
            database.create_configuration(
                config_id=config_id,
                devices=devices,
                unhandled_warnings=errors.unhandledDevicesWarnings,
                device_warnings=errors.deviceWarnings,
                misc_warnings=errors.misconfigurationWarnings,
                is_public=True,
                **meta,
            )
        known_ids.add(config_id)
        report.imported.append(config_id)
    return report
