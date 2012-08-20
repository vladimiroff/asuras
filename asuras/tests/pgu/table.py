import unittest

import sys; sys.path.insert(0, "../..")
from pgu import gui

class TableTest(unittest.TestCase):

    def setUp(self):
        self.table = gui.Table(width=200, height=200)

    def test_init(self):
        self.assertTrue(self.table.cls, 'table')

    def test_basic_app(self):
        button = gui.Button('Test')
        self.table.add(button, 0, 0)
        self.assertTrue(self.table._trok)

if __name__ == '__main__':
    unittest.main()
