import unittest

from canvas import Color
from matrix import Identity_Matrix, Scaling_Matrix, Translation_Matrix
from pattern import CheckerPattern, GradientPattern, RingPattern, StripePattern, TestPattern
from shape import Sphere
from tuple import Point

class PatternTestCase(unittest.TestCase):

  def setUp(self):
    self.black = Color(0, 0, 0)
    self.white = Color(1, 1, 1)

  def test_test_pattern(self):
    pattern = TestPattern()
    self.assertEqual(pattern.transform, Identity_Matrix(4))
    pattern.set_transform(Translation_Matrix(1, 2, 3))
    self.assertEqual(pattern.transform, Translation_Matrix(1, 2, 3))
    pattern = TestPattern()
    shape = Sphere()
    shape.transform = Scaling_Matrix(2, 2, 2)
    c = pattern.pattern_at_shape(shape, Point(2, 3, 4))
    self.assertTrue(c.equals(Color(1, 1.5, 2)))
    pattern = TestPattern()
    pattern.transform = Scaling_Matrix(2, 2, 2)
    shape = Sphere()
    c = pattern.pattern_at_shape(shape, Point(2, 3, 4))
    self.assertTrue(c.equals(Color(1, 1.5, 2)))
    pattern = TestPattern()
    pattern.transform = Translation_Matrix(0.5, 1, 1.5)
    shape = Sphere()
    shape.transform = Scaling_Matrix(2, 2, 2)
    c = pattern.pattern_at_shape(shape, Point(2.5, 3, 3.5))
    self.assertTrue(c.equals(Color(0.75, 0.5, 0.25)))

  def test_stripe_pattern(self):
    pattern = StripePattern(self.white, self.black)
    self.assertTrue(pattern.ca.equals(self.white))
    self.assertTrue(pattern.cb.equals(self.black))
    self.assertTrue(pattern.pattern_at(Point(0, 0, 0)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(0, 1, 0)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(0, 2, 0)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(0, 0, 1)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(0, 0, 2)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(0.9, 0, 0)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(1, 0, 0)).equals(self.black))
    self.assertTrue(pattern.pattern_at(Point(-0.1, 0, 0)).equals(self.black))
    self.assertTrue(pattern.pattern_at(Point(-1, 0, 0)).equals(self.black))
    self.assertTrue(pattern.pattern_at(Point(-1.1, 0, 0)).equals(self.white))

  def test_gradient_pattern(self):
    pattern = GradientPattern(self.white, self.black)
    self.assertTrue(pattern.pattern_at(Point(0, 0, 0)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(0.25, 0, 0)).equals(Color(0.75, 0.75, 0.75)))
    self.assertTrue(pattern.pattern_at(Point(0.5, 0, 0)).equals(Color(0.5, 0.5, 0.5)))
    self.assertTrue(pattern.pattern_at(Point(0.75, 0, 0)).equals(Color(0.25, 0.25, 0.25)))

  def test_ring_pattern(self):
    pattern = RingPattern(self.white, self.black)
    self.assertTrue(pattern.pattern_at(Point(0, 0, 0)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(1, 0, 0)).equals(self.black))
    self.assertTrue(pattern.pattern_at(Point(0, 0, 1)).equals(self.black))
    self.assertTrue(pattern.pattern_at(Point(0.708, 0, 0.708)).equals(self.black))

  def test_checker_pattern(self):
    pattern = CheckerPattern(self.white, self.black)
    self.assertTrue(pattern.pattern_at(Point(0, 0, 0)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(0.99, 0, 0)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(1.01, 0, 0)).equals(self.black))
    self.assertTrue(pattern.pattern_at(Point(0, 0.99, 0)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(0, 1.01, 0)).equals(self.black))
    self.assertTrue(pattern.pattern_at(Point(0, 0, 0.99)).equals(self.white))
    self.assertTrue(pattern.pattern_at(Point(0, 0, 1.01)).equals(self.black))
