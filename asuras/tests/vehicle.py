import unittest

from vehicle import Vehicle
from vehicle.types.normal import NormalVehicle
from vehicle.components import VehicleComponent


class BaseVehicleTests(unittest.TestCase):

    def setUp(self):
        self.vehicle = Vehicle((10, 10))
        self.normal = NormalVehicle((10, 10))
        self.component = VehicleComponent()
        self.component.group = 'engines'

    def test_defaults(self):
        self.assertIsInstance(self.vehicle.DEFAULTS, dict)

    def test_component_could_be_attach(self):
        self.assertEqual(len(self.vehicle._slots), 0)
        self.vehicle.attach(self.component, 'front')
        self.assertEqual(len(self.vehicle._slots), 1)

    def test_component_detach(self):
        self.vehicle.attach(self.component, 'front')
        self.assertEqual(len(self.vehicle._slots[self.component.group]), 1)
        self.vehicle.detach(self.component, 'front')
        self.assertEqual(len(self.vehicle._slots[self.component.group]), 0)
