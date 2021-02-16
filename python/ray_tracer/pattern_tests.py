import unittest

from canvas import Color
from matrix import Identity_Matrix, Scaling_Matrix, Translation_Matrix
from pattern import TestPattern
from shape import Sphere
from tuple import Point

class PatternTestCase(unittest.TestCase):

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