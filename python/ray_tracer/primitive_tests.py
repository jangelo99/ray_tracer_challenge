import math
import unittest

from matrix import Identity_Matrix, Translation_Matrix
from primitive import Sphere
from ray_tracer import Ray
from tuple import Point, Vector

class PrimitiveTestCase(unittest.TestCase):

  def test_sphere_intersect(self):
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    xs = s.intersect(r)
    self.assertEqual(len(xs), 2)
    self.assertEqual(xs[0], 4.0)
    self.assertEqual(xs[1], 6.0)
    r = Ray(Point(0, 1, -5), Vector(0, 0, 1))
    xs = s.intersect(r)
    self.assertEqual(len(xs), 2)
    self.assertEqual(xs[0], 5.0)
    self.assertEqual(xs[1], 5.0)
    r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
    xs = s.intersect(r)
    self.assertEqual(len(xs), 0)
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    xs = s.intersect(r)
    self.assertEqual(len(xs), 2)
    self.assertEqual(xs[0], -1.0)
    self.assertEqual(xs[1], 1.0)
    r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
    xs = s.intersect(r)
    self.assertEqual(len(xs), 2)
    self.assertEqual(xs[0], -6.0)
    self.assertEqual(xs[1], -4.0)

  def test_sphere_transform(self):
    s = Sphere()
    self.assertEqual(s.transform, Identity_Matrix(4))
    translation = Translation_Matrix(2, 3, 4)
    s.set_transform(translation)
    self.assertEqual(s.transform, translation)

  def test_normal_at(self):
    s = Sphere()
    n = s.normal_at(Point(1, 0, 0))
    self.assertTrue(n.equals(Vector(1, 0, 0)))
    n = s.normal_at(Point(0, 1, 0))
    self.assertTrue(n.equals(Vector(0, 1, 0)))
    n = s.normal_at(Point(0, 0, 1))
    self.assertTrue(n.equals(Vector(0, 0, 1)))
    n = s.normal_at(Point(math.sqrt(3)/3.0, math.sqrt(3)/3.0, math.sqrt(3)/3.0))
    self.assertTrue(n.equals(Vector(math.sqrt(3)/3.0, math.sqrt(3)/3.0, math.sqrt(3)/3.0)))
    self.assertEqual(n.magnitude(), 1.0)
