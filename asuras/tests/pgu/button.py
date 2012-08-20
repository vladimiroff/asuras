import unittest

import sys; sys.path.insert(0, "../..")
from pgu import gui

class ButtonTest(unittest.TestCase):

    def setUp(self):
        self.app = gui.app.App()
        self.button = gui.Button("Test")

if __name__ == '__main__':
    unittest.main()
