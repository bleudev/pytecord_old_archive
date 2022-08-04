import unittest

print("For test")

def import_disspy():
    import disspy

class TestInit(unittest.TestCase):
    def test(self):
        self.assertRaises(Exception, import_disspy)

unittest.main()
