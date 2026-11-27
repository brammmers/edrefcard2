"""A hardware ID attached to a legacy template must get that template's boxes."""
import copy
import unittest

import scripts.bindingsData as bindings_data


class LegacyAliasTests(unittest.TestCase):
    def setUp(self):
        # Attaching mutates the shared registries in place: restore them after
        # each test, keeping the same objects other modules imported.
        self.data = bindings_data
        self._devices = copy.deepcopy(bindings_data.supportedDevices)
        self._details = set(bindings_data.hotasDetails)

    def tearDown(self):
        bindings_data.supportedDevices.clear()
        bindings_data.supportedDevices.update(self._devices)
        for key in set(bindings_data.hotasDetails) - self._details:
            del bindings_data.hotasDetails[key]

    def test_attached_id_gets_the_template_boxes(self):
        # VIRPIL bases report a new ID per base/firmware; 33444130 is a
        # Constellation Alpha R on a MongoosT-50CM2 base.
        self.assertNotIn('33444130', self.data.hotasDetails)
        self.data.apply_legacy_device_aliases(
            [{'device_id': '33444130', 'legacy_key': 'VPC-ALPHA-Right'}])
        target = self.data.supportedDevices['VPC-ALPHA-Right']
        self.assertIn('33444130', target['HandledDevices'])
        boxes = self.data.hotasDetails['33444130']
        self.assertEqual(boxes['Joy_13'], self.data.hotasDetails['3344412F']['Joy_13'])
        # every ID the template loops over has boxes (the template preview
        # indexes hotasDetails directly)
        for device in target.get('KeyDevices', target['HandledDevices']):
            self.assertIn(device, self.data.hotasDetails)

    def test_repeated_attach_and_unknown_template_are_harmless(self):
        aliases = [{'device_id': '3344812F', 'legacy_key': 'VPC-ALPHA-Left'},
                   {'device_id': '3344812F', 'legacy_key': 'VPC-ALPHA-Left'},
                   {'device_id': 'DEAD0001', 'legacy_key': 'NoSuchTemplate'}]
        self.data.apply_legacy_device_aliases(aliases)
        handled = self.data.supportedDevices['VPC-ALPHA-Left']['HandledDevices']
        self.assertEqual(handled.count('3344812F'), 1)
        self.assertIn('3344812F', self.data.hotasDetails)
        self.assertNotIn('DEAD0001', self.data.hotasDetails)


if __name__ == '__main__':
    unittest.main()
