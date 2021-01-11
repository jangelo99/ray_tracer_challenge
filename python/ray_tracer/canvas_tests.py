import unittest

from canvas import Color


class CanvasTestCase(unittest.TestCase):

  def setUp(self):
    self.c1 = Color(0.9, 0.6, 0.75)
    self.c2 = Color(0.7, 0.1, 0.25)

  def test_color(self):
    c = Color(-0.5, 0.4, 1.7)
    self.assertEqual(c.r, -0.5)
    self.assertEqual(c.g, 0.4)
    self.assertEqual(c.b, 1.7)

  def test_color_operations(self):
    result = self.c1.add(self.c2)
    self.assertTrue(result.equals(Color(1.6, 0.7, 1.0)))
    result = self.c1.subtract(self.c2)
    self.assertTrue(result.equals(Color(0.2, 0.5, 0.5)))
    c = Color(0.2, 0.3, 0.4)
    result = c.scalar_multiply(2.0)
    self.assertTrue(result.equals(Color(0.4, 0.6, 0.8)))
    c1 = Color(1.0, 0.2, 0.4)
    c2 = Color(0.9, 1.0, 0.1)
    result = c1.hadamard_product(c2)
    self.assertTrue(result.equals(Color(0.9, 0.2, 0.04)))
