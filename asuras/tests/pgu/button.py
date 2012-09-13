import unittest

import sys; sys.path.insert(0, "../..")
from pgu import gui

class ButtonTest(unittest.TestCase):

    def setUp(self):
        self.app = gui.app.App()
        self.button = gui.Button("Test")

    def test_basic_attributes(self):
        assert self.button.focusable is True
        assert self.button.cls == 'button'
        assert isinstance(self.button.value, gui.Label)


class SwitchTest(unittest.TestCase):

    def setUp(self):
        self.switch = gui.Switch('Toggle')

    def test_basic_attributes(self):
        assert self.switch.focusable is True
        assert self.switch.cls == 'switch'
        assert isinstance(self.switch.value, str)

if __name__ == '__main__':
    unittest.main()
