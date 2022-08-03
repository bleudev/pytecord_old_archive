import unittest

def import_disspy():
    import disspy

class TestInit(unittest.TestCase):
    def test(self):
        self.assertRaises(Exception, import_disspy)

if __name__ == "__main__":
    unittest.main()
