import unittest

from matrix import Identity_Matrix, Scaling_Matrix, Translation_Matrix
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

  def test_ray_intersect(self):
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    r.intersect(s)
    xs = r.intersections
    self.assertEqual(len(xs), 2)
    self.assertEqual(xs[0].t, 4.0)
    self.assertEqual(xs[0].shape, s)
    self.assertEqual(xs[1].t, 6.0)
    self.assertEqual(xs[1].shape, s)

  def test_ray_hit(self):
    s = Sphere()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    r.intersect(s)
    hit = r.hit()
    self.assertEqual(hit, Intersection(4, s))
    r = Ray(Point(0, 2, -5), Vector(0, 0, 1))
    r.intersect(s)
    hit = r.hit()
    self.assertEqual(hit, None)
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    r.intersect(s)
    hit = r.hit()
    self.assertEqual(hit, Intersection(1, s))
    r = Ray(Point(0, 0, 5), Vector(0, 0, 1))
    r.intersect(s)
    hit = r.hit()
    self.assertEqual(hit, None)

  def test_sphere_transform(self):
    s = Sphere()
    self.assertEqual(s.transform, Identity_Matrix(4))
    translation = Translation_Matrix(2, 3, 4)
    s.set_transform(translation)
    self.assertEqual(s.transform, translation)

  def test_ray_transform(self):
    r = Ray(Point(1, 2, 3), Vector(0, 1, 0))
    m = Translation_Matrix(3, 4, 5)
    r2 = r.transform(m)
    self.assertTrue(r2.origin.equals(Point(4, 6, 8)))
    self.assertTrue(r2.direction.equals(Vector(0, 1, 0)))
    m = Scaling_Matrix(2, 3, 4)
    r3 = r.transform(m)
    self.assertTrue(r3.origin.equals(Point(2, 6, 12)))
    self.assertTrue(r3.direction.equals(Vector(0, 3, 0)))

  def test_ray_transformed_sphere_intersect(self):
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = Sphere()
    s.set_transform(Scaling_Matrix(2, 2, 2))
    r.intersect(s)
    xs = r.intersections
    self.assertEqual(len(xs), 2)
    self.assertEqual(xs[0].t, 3.0)
    self.assertEqual(xs[1].t, 7.0)
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s.set_transform(Translation_Matrix(5, 0, 0))
    r.intersect(s)
    xs = r.intersections
    self.assertEqual(len(xs), 0)
