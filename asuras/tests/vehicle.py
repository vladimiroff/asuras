import unittest

from vehicle import Vehicle
from vehicle.types import NormalVehicle

class BaseVehicleTests(unittest.TestCase):

    def setUp(self):
        self.v = Vehicle()
        self.n = NormalVehicle()

    def test_defaults(self):
        self.assertIsInstance(self.v.DEFAULTS, dict)

    def test_component_could_be_attach(self):
        pass

