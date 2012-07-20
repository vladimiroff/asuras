import unittest

from vehicle import Vehicle
from vehicle.types.normal import NormalVehicle

class BaseVehicleTests(unittest.TestCase):

    def setUp(self):
        self.v = Vehicle((10, 10))
        self.n = NormalVehicle((10, 10))

    def test_defaults(self):
        self.assertIsInstance(self.v.DEFAULTS, dict)

    def test_component_could_be_attach(self):
        pass

