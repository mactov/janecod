import unittest
from InteractiveShell import InteractiveShell

class InteractiveShellTest(unittest.TestCase):
    def setUp(self):
        self.intsh = InteractiveShell()

    def test_roll(self):
        pass
        # ## roll gets an integer and returns:
        # ## Buzz if its input is a multiple of 3
        # ## Fizz if its input is a multiple of 5
        # ## the string version of the integer
        # self.assertEqual(self.bf.roll(1),'1')
        # self.assertEqual(self.bf.roll(2),'2')
        # self.assertEqual(self.bf.roll(3),'Buzz')
        # self.assertEqual(self.bf.roll(4),'4')
        # self.assertEqual(self.bf.roll(5), 'Fizz')
        # self.assertEqual(self.bf.roll(6),'Buzz')
        # self.assertEqual(self.bf.roll(15), 'Buzz Fizz')

if __name__ == '__main__':
    unittest.main()