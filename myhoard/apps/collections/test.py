import unittest


class Test(unittest.TestCase):
    """
    TODO testing search
    python -m unittest test.Test
    """

    def setUp(self):
        pass

    def test_demo(self):
        self.assertEqual(13, 13)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()