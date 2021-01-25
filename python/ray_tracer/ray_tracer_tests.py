import ray_tracer
import unittest

from primitive import Sphere
from ray_tracer import Intersection, Ray
from tuple import Point, Vector

class RayTracerTestCase(unittest.TestCase):

  def test_ray_position(self):
    r = Ray(Point(2, 3, 4), Vector(1, 0, 0))
    p = r.position(0)
    self.assertTrue(p.equals(Point(2, 3, 4)))
    p = r.position(1)
    self.assertTrue(p.equals(Point(3, 3, 4)))
    p = r.position(-1)
    self.assertTrue(p.equals(Point(1, 3, 4)))
    p = r.position(2.5)
    self.assertTrue(p.equals(Point(4.5, 3, 4)))

  def test_ray_sphere_intersect(self):
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

  def test_intersect_function(self):
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    xs = ray_tracer.intersect(s, r)
    self.assertEqual(len(xs), 2)
    self.assertEqual(xs[0].t, 4.0)
    self.assertEqual(xs[0].shape, s)
    self.assertEqual(xs[1].t, 6.0)
    self.assertEqual(xs[1].shape, s)
