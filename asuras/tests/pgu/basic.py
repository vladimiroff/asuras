import unittest

import sys; sys.path.insert(0, "../..")
from pgu import gui

class LabelTest(unittest.TestCase):
    '''
    TODO: Test fonts
    '''

    def setUp(self):
        self.label = gui.Label('Lama')

    def test_basic_attributes(self):
        assert self.label.focusable is False
        assert self.label.cls == 'label'
        assert self.label.value == 'Lama'

    def test_set_text(self):
        assert self.label.value == 'Lama'
        self.label.set_text('Duck')
        assert self.label.value == 'Duck'

if __name__ == '__main__':
    unittest.main()
