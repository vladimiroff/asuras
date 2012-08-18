import unittest

import sys; sys.path.insert(0, "../..")
from pgu import gui

class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = gui.app.App()

    def test_init_app(self):
        self.assertTrue(hasattr(self.app, 'theme'))
        self.assertEqual(self.app.cls, 'default')

    def test_init_desktop(self):
        desktop = gui.app.Desktop()
        self.assertEqual(desktop.cls, 'desktop')

    def test_global_app(self):
        self.assertEqual(self.app, gui.pguglobals.app)
        self.assertEqual(self.app, gui.app.App.app)

    # TODO: This belongs to widget's tests(when they appear)
    def test_connect(self):
        self.assertEqual(self.app.connects, {})
        self.app.connect(gui.QUIT, self.app.quit)
        self.assertTrue(gui.QUIT in self.app.connects)


if __name__ == '__main__':
    unittest.main()
