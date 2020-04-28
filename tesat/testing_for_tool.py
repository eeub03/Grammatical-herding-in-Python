from Herd import Herd_Member, Herd
from parameters.parameters import params
from mapping import Mapper, Genotype, Key_Gen



import unittest


class HerdMethods(unittest.TestCase):
    def setUp(self):
        self.herd = Herd.Herd()
    def test_creation(self):
        self.assertIsNotNone(self.herd.herd)
    def test_evaluation(self):

if __name__ == '__main__':
    unittest.main()