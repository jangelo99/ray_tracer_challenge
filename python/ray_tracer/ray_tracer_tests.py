import math
import unittest

from canvas import Color
from matrix import Scaling_Matrix, Translation_Matrix
from primitive import Material, Sphere
from ray_tracer import Intersection, PointLight, Ray
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

  def test_lighting_at(self):
    m = Material()
    position = Point(0, 0, 0)
    intensity = Color(1, 1, 1)
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), intensity)
    result = light.lighting_at(m, position, eyev, normalv)
    self.assertTrue(result.equals(Color(1.9, 1.9, 1.9)))
    eyev = Vector(0, math.sqrt(2.0)/2.0, -1*math.sqrt(2.0)/2.0)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), intensity)
    result = light.lighting_at(m, position, eyev, normalv)
    self.assertTrue(result.equals(Color(1.0, 1.0, 1.0)))
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), intensity)
    result = light.lighting_at(m, position, eyev, normalv)
    self.assertTrue(result.equals(Color(0.7364, 0.7364, 0.7364)))
    eyev = Vector(0, -1*math.sqrt(2.0)/2.0, -1*math.sqrt(2.0)/2.0)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 10, -10), intensity)
    result = light.lighting_at(m, position, eyev, normalv)
    self.assertTrue(result.equals(Color(1.6364, 1.6364, 1.6364)))
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, 10), intensity)
    result = light.lighting_at(m, position, eyev, normalv)
    self.assertTrue(result.equals(Color(0.1, 0.1, 0.1)))
