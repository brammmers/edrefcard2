"""Import the cards of the historical live site (edrefcard.info).

The live site stored every card as configs/<id[:2]>/<id>.binds plus a pickled
<id>.replay (saveReplayInfo in the upstream bindings.py): a dict holding the
title, styling, display groups, timestamp, devices and warnings.

This module copies the .binds sources into our configs folder and recreates
the database rows with the original id, title, styling, display groups and
date, so every /binds/<id> link shared on the forums keeps working. Cards
that never got a .replay (no title given) are imported unlisted. Devices
and warnings are recomputed from the .binds with the current parser, which
knows more controllers than the live one did.

An id that already exists here is only touched when it is the same card
(same_card): an earlier, degraded import of the old backup is then replaced
by the original (file, title, date, visibility; view count kept) and
reported as "refreshed", or skipped as "duplicate" when already up to date.
A different card under the same id is never overwritten ("clash").
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
BOM = b'\xef\xbb\xbf'

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
    imported_unlisted: list = field(default_factory=list)
    refreshed: list = field(default_factory=list)
    duplicates: list = field(default_factory=list)
    clashes: list = field(default_factory=list)
    missing_binds: list = field(default_factory=list)
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


def same_card(a, b):
    """True when two .binds hold the same card, line endings and blank lines aside.

    The January 2026 import of the old backup doubled every line ending
    (a blank line after each line); its cards are the same as the originals.
    """
    def lines(raw):
        raw = raw.removeprefix(BOM).replace(b'\r', b'\n')
        return [line.strip() for line in raw.split(b'\n') if line.strip()]
    return lines(a) == lines(b)


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


def _unlisted_metadata(source):
    """Defaults the live replay mode used for a .binds without .replay.

    The live site only wrote a .replay for published cards (a title was
    given), yet served /binds/<id> for every .binds: its replay check was
    `replayPath.exists` without parentheses, always true. Those cards keep
    working here as unlisted cards, drawn with the same default groups.
    """
    mtime = datetime.datetime.fromtimestamp(source.stat().st_mtime, datetime.UTC)
    return {
        'description': '',
        'styling': 'None',
        'display_groups': list(LIVE_DEFAULT_GROUPS),
        'created_at': mtime.isoformat(' '),
    }


def import_live_configs(source_dir, dry_run=False, limit=None, log=None):
    """Import every card found under source_dir.

    <id>.binds + <id>.replay is a published card (listed, original metadata);
    a lone <id>.binds is an unlisted card (live defaults, file date).
    Returns an ImportReport. With dry_run, nothing is written but every
    check (replay, parser, collisions) still runs.
    """
    report = ImportReport(dry_run=dry_run)
    replays = _index(source_dir, '.replay', report)
    binds = _index(source_dir, '.binds', report)
    known_ids = set(database.get_all_config_ids())
    configs_root = Config.configsPath()
    all_ids = sorted(set(replays) | set(binds))

    processed = 0
    for config_id in all_ids:
        if limit is not None and processed >= limit:
            break
        processed += 1
        if log and processed % 1000 == 0:
            log(f'{processed}/{len(all_ids)}...')

        if not Config.isValidName(config_id):
            report.invalid_ids.append(config_id)
            continue
        source = binds.get(config_id)
        if source is None:
            report.missing_binds.append(config_id)
            continue
        listed = config_id in replays
        if listed:
            try:
                meta = replay_metadata(load_replay(replays[config_id]))
            except ReplayError as exc:
                report.bad_replays.append({'id': config_id, 'error': str(exc)})
                continue
        else:
            meta = _unlisted_metadata(source)

        raw = source.read_bytes()
        if len(raw) > MAX_BINDS_BYTES:
            report.parse_errors.append({'id': config_id, 'error': 'file too large'})
            continue
        target = Config(config_id).pathWithSuffix('.binds')
        refresh = config_id in known_ids or target.exists()
        if refresh:
            existing = target.read_bytes() if target.exists() else None
            if existing is not None and not same_card(existing, raw):
                report.clashes.append(config_id)
                continue
            row = database.get_configuration(config_id)
            if (existing == raw and row is not None
                    and row['description'] == meta['description']
                    and str(row['created_at']) == str(meta['created_at'])
                    and bool(row['is_public']) == listed):
                report.duplicates.append(config_id)  # already imported
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
            save = database.replace_configuration if refresh else database.create_configuration
            save(
                config_id=config_id,
                devices=devices,
                unhandled_warnings=errors.unhandledDevicesWarnings,
                device_warnings=errors.deviceWarnings,
                misc_warnings=errors.misconfigurationWarnings,
                is_public=listed,
                **meta,
            )
        known_ids.add(config_id)
        if refresh:
            report.refreshed.append(config_id)
        else:
            (report.imported if listed else report.imported_unlisted).append(config_id)
    return report
