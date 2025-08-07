import unittest

from calculator import calculate


class TestCalculator(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(calculate("2 + 3 * 4"), 14)
        self.assertEqual(calculate("(2 + 3) * 4"), 20)
        self.assertAlmostEqual(calculate("7 / 2"), 3.5)
        self.assertEqual(calculate("7 // 2"), 3)
        self.assertEqual(calculate("7 % 4"), 3)

    def test_power_and_unary(self):
        self.assertEqual(calculate("2 ** 5"), 32)
        self.assertEqual(calculate("-5 + +2"), -3)

    def test_math_functions(self):
        self.assertAlmostEqual(calculate("sqrt(9)"), 3.0)
        self.assertAlmostEqual(calculate("sin(pi/2)"), 1.0, places=7)
        self.assertAlmostEqual(calculate("log(e)"), 1.0, places=7)
        self.assertEqual(calculate("round(3.14159, 2)"), 3.14)

    def test_min_max_abs(self):
        self.assertEqual(calculate("min(3, -5, 10)"), -5)
        self.assertEqual(calculate("max(3, -5, 10)"), 10)
        self.assertEqual(calculate("abs(-7)"), 7)

    def test_disallowed_name(self):
        with self.assertRaises(ValueError):
            calculate("__import__('os').system('echo hacked')")
        with self.assertRaises(ValueError):
            calculate("open")


if __name__ == "__main__":
    unittest.main()