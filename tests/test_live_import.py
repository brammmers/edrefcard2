"""Import of the old live site's cards (.binds + pickled .replay pairs)."""
import datetime
import os
import pickle
import tempfile
import unittest
from collections import OrderedDict
from pathlib import Path

from scripts import database, live_import
from scripts.models import Config

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = (ROOT / 'bindings' / 'Defaults 3.3' / 'SaitekX52.binds').read_bytes()
OTHER = (ROOT / 'bindings' / 'Defaults 3.3' / 'T16000MHOTAS.binds').read_bytes()
STAMP = datetime.datetime(2025, 3, 14, 9, 26, 53, tzinfo=datetime.timezone.utc)


class Exploit:
    """A replay that would run a command if loaded with pickle.load."""
    def __reduce__(self):
        return (os.system, ('echo pwned',))


def live_replay(**overrides):
    # Same shape as saveReplayInfo() in the upstream bindings.py.
    data = {
        'displayGroups': ['Ship', 'UI', 'Galaxy map'],
        'misconfigurationWarnings': '',
        'unhandledDevicesWarnings': '',
        'deviceWarnings': '',
        'styling': 'Group',
        'description': 'My X52 setup',
        'timestamp': STAMP,
        'devices': OrderedDict([('SaitekX52', None)]),
    }
    data.update(overrides)
    return data


class LiveImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='edrefcard-live-import-',
                                                ignore_cleanup_errors=True)
        base = Path(self.temp.name)
        self.source = base / 'live' / 'configs'
        self.configs = base / 'configs'
        self.configs.mkdir()
        self.saved_configs = Config._configs_path
        self.saved_db = database.DB_PATH
        Config.setConfigsPath(self.configs)
        database.init_db(base / 'test.db')

    def tearDown(self):
        Config._configs_path = self.saved_configs
        database.DB_PATH = self.saved_db
        self.temp.cleanup()

    def add_card(self, config_id, replay=None, binds=SAMPLE):
        folder = self.source / config_id[:2]
        folder.mkdir(parents=True, exist_ok=True)
        if binds is not None:
            (folder / f'{config_id}.binds').write_bytes(binds)
        if replay is not None:
            with (folder / f'{config_id}.replay').open('wb') as handle:
                pickle.dump(replay, handle)

    def run_import(self, **kwargs):
        return live_import.import_live_configs(self.source, **kwargs)

    def test_card_keeps_its_id_title_styling_groups_and_date(self):
        self.add_card('abcdef', live_replay())
        report = self.run_import()
        self.assertEqual(report.imported, ['abcdef'])
        row = database.get_configuration('abcdef')
        self.assertEqual(row['description'], 'My X52 setup')
        self.assertEqual(row['styling'], 'Group')
        self.assertEqual(sorted(row['display_groups']), ['Galaxy map', 'Ship', 'UI'])
        self.assertTrue(str(row['created_at']).startswith('2025-03-14 09:26:53'))
        self.assertEqual(row['is_public'], 1)
        self.assertIn('SaitekX52::0', row['devices'])
        self.assertEqual(Config('abcdef').pathWithSuffix('.binds').read_bytes(), SAMPLE)

    def test_dry_run_checks_everything_and_writes_nothing(self):
        self.add_card('abcdef', live_replay())
        report = self.run_import(dry_run=True)
        self.assertEqual(report.imported, ['abcdef'])
        self.assertIsNone(database.get_configuration('abcdef'))
        self.assertFalse(Config('abcdef').pathWithSuffix('.binds').exists())

    def test_existing_ids_are_never_overwritten(self):
        database.create_configuration('samesm', description='beta card')
        target = Config('samesm').pathWithSuffix('.binds')
        target.parent.mkdir(parents=True)
        target.write_bytes(SAMPLE)
        database.create_configuration('clashx', description='beta card')
        clash = Config('clashx').pathWithSuffix('.binds')
        clash.parent.mkdir(parents=True)
        clash.write_bytes(OTHER)
        self.add_card('samesm', live_replay())
        self.add_card('clashx', live_replay())

        report = self.run_import()
        self.assertEqual(report.duplicates, ['samesm'])
        self.assertEqual(report.clashes, ['clashx'])
        self.assertEqual(report.imported, [])
        self.assertEqual(clash.read_bytes(), OTHER)
        self.assertEqual(database.get_configuration('clashx')['description'], 'beta card')

    def test_malicious_replay_is_rejected_without_running(self):
        self.add_card('evilxx', {'description': Exploit()})
        report = self.run_import()
        self.assertEqual([item['id'] for item in report.bad_replays], ['evilxx'])
        self.assertIn('forbidden global', report.bad_replays[0]['error'])
        self.assertIsNone(database.get_configuration('evilxx'))

    def test_corrupt_replay_is_reported(self):
        self.add_card('brokex')
        (self.source / 'br' / 'brokex.replay').write_bytes(b'\x80\x04not a pickle')
        report = self.run_import()
        self.assertEqual([item['id'] for item in report.bad_replays], ['brokex'])

    def test_replay_without_binds_is_reported(self):
        self.add_card('nobind', live_replay(), binds=None)
        report = self.run_import()
        self.assertEqual(report.missing_binds, ['nobind'])
        self.assertEqual(report.imported, [])

    def test_lone_binds_becomes_an_unlisted_card_with_live_defaults(self):
        # The live site served /binds/<id> for cards without a .replay.
        self.add_card('noreply')
        source = self.source / 'no' / 'noreply.binds'
        stamp = datetime.datetime(2024, 7, 19, 17, 3, tzinfo=datetime.timezone.utc).timestamp()
        os.utime(source, (stamp, stamp))
        report = self.run_import()
        self.assertEqual(report.imported_unlisted, ['noreply'])
        self.assertEqual(report.imported, [])
        row = database.get_configuration('noreply')
        self.assertEqual(row['is_public'], 0)
        self.assertEqual(row['description'], '')
        self.assertEqual(sorted(row['display_groups']), sorted(live_import.LIVE_DEFAULT_GROUPS))
        self.assertTrue(str(row['created_at']).startswith('2024-07-19 17:03:00'))
        self.assertEqual(Config('noreply').pathWithSuffix('.binds').read_bytes(), SAMPLE)

    def test_ids_that_could_escape_the_configs_folder_are_refused(self):
        folder = self.source / 'xx'
        folder.mkdir(parents=True)
        (folder / 'bad id.binds').write_bytes(SAMPLE)
        with (folder / 'bad id.replay').open('wb') as handle:
            pickle.dump(live_replay(), handle)
        report = self.run_import()
        self.assertEqual(report.invalid_ids, ['bad id'])

    def test_old_replays_get_the_live_defaults(self):
        data = live_replay(styling='Weird', description=None,
                           timestamp=datetime.datetime(2019, 1, 2, 3, 4, 5))
        del data['displayGroups']
        self.add_card('oldone', data)
        self.run_import()
        row = database.get_configuration('oldone')
        self.assertEqual(row['styling'], 'None')
        self.assertEqual(row['description'], '')
        self.assertEqual(sorted(row['display_groups']), sorted(live_import.LIVE_DEFAULT_GROUPS))
        self.assertTrue(str(row['created_at']).startswith('2019-01-02 03:04:05'))

    def test_limit_stops_early(self):
        for config_id in ('aaaaaa', 'bbbbbb', 'cccccc'):
            self.add_card(config_id, live_replay())
        report = self.run_import(limit=2)
        self.assertEqual(report.imported, ['aaaaaa', 'bbbbbb'])

    def test_command_is_registered(self):
        source = (ROOT / 'www' / 'app.py').read_text(encoding='utf-8')
        self.assertIn('app.cli.add_command(import_live_command)', source)


if __name__ == '__main__':
    unittest.main()
