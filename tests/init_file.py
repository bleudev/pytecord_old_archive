import unittest

def import_disspy():
    import disspy

class TestInit(unittest.TestCase):
    def test(self):
        self.assertRaises(Exception, import_disspy)

unittest.main()
