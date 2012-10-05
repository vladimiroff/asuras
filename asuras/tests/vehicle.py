import unittest

from vehicle import Vehicle
from vehicle.types.normal import NormalVehicle
from vehicle.components import VehicleComponent
from libs import tmx

class BaseVehicleTests(unittest.TestCase):

    def setUp(self):
        self.sprites = tmx.layers.SpriteLayer()
        self.items = tmx.layers.SpriteLayer()
        self.v = Vehicle((10, 10), self.items, self.sprites)
        self.n = NormalVehicle((10, 10), self.items, self.sprites)
        self.component = VehicleComponent('motions')

    def test_defaults(self):
        self.assertIsInstance(self.v.DEFAULTS, dict)

    def test_component_could_be_attach(self):
        self.assertIsNone(self.v._slots['motions'].get(0, None))
        self.v.attach(VehicleComponent('motions'), 0)
        self.assertIsNotNone(self.v._slots['motions'].get(0, None))

    def test_try_to_attach_on_existing_slot(self):
        attached_component = self.v.attach(self.component, 0)
        second_component = VehicleComponent('motions')
        self.v.attach(second_component, 0)
        self.assertIs(self.v._slots[self.component.group][0], attached_component)
        self.assertIsNot(self.v._slots['motions'][0], second_component)

    def test_try_to_attach_on_existing_slot_using_overwrite(self):
        attached_component = self.v.attach(self.component, 0)
        second_component = VehicleComponent('motions')
        self.v.attach(second_component, 0, overwrite=True)
        self.assertIsNot(self.v._slots[self.component.group][0], attached_component)
        self.assertIs(self.v._slots['motions'][0], second_component)

    def test_detach(self):
        self.v.attach(self.component, 0)
        self.v.detach(self.component, 0)
        self.assertIsNone(self.v._slots['motions'].get(0, None))

    def test_recalculation(self):
        self.assertEqual(self.v.weight, 0)
        self.v.attach(self.component, 0)
        self.assertGreater(self.v.weight, 0)

