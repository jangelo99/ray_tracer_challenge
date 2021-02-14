import math
import unittest

from canvas import Color
from matrix import Identity_Matrix, Rotation_Axis, Rotation_Matrix, Scaling_Matrix, Translation_Matrix
from ray_tracer import Ray
from shape import Material, Sphere, TestShape
from tuple import Point, Vector

class ShapeTestCase(unittest.TestCase):

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
    # test normals on transformed sphere
    s = Sphere()
    s.set_transform(Translation_Matrix(0, 1, 0))
    n = s.normal_at(Point(0, 1.70711, -0.70711))
    self.assertTrue(n.equals(Vector(0, 0.70711, -0.70711)))
    s = Sphere()
    m = Scaling_Matrix(1, 0.5, 1) * Rotation_Matrix(Rotation_Axis.Z, 36)
    s.set_transform(m)
    n = s.normal_at(Point(0, math.sqrt(2)/2.0, -1.0 * math.sqrt(2)/2.0))
    self.assertTrue(n.equals(Vector(0, 0.97014, -0.24254)))

  def test_default_material(self):
    m = Material()
    self.assertTrue(m.color.equals(Color(1.0, 1.0, 1.0)))
    self.assertEqual(m.ambient, 0.1)
    self.assertEqual(m.diffuse, 0.9)
    self.assertEqual(m.specular, 0.9)
    self.assertEqual(m.shininess, 200.0)

  def test_sphere_material(self):
    s = Sphere()
    m = Material()
    self.assertTrue(s.material.equals(m))
    s = Sphere()
    m = Material()
    m.ambient = 1.0
    s.material = m
    self.assertEqual(s.material.ambient, 1.0)
    self.assertTrue(s.material.equals(m))

  def test_test_shape(self):
    s = TestShape()
    self.assertEqual(s.transform, Identity_Matrix(4))
    translation = Translation_Matrix(2, 3, 4)
    s.set_transform(translation)
    self.assertEqual(s.transform, translation)
    self.assertTrue(s.material.equals(Material()))
    m = Material()
    m.ambient = 1
    s.material = m
    self.assertTrue(s.material.equals(m))

  def test_shape_intersect(self):
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = TestShape()
    s.set_transform(Scaling_Matrix(2, 2, 2))
    xs = s.intersect(r)
    self.assertTrue(s.local_ray.origin.equals(Point(0, 0, -2.5)))
    self.assertTrue(s.local_ray.direction.equals(Vector(0, 0, 0.5)))
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    s = TestShape()
    s.set_transform(Translation_Matrix(5, 0, 0))
    xs = s.intersect(r)
    self.assertTrue(s.local_ray.origin.equals(Point(-5, 0, -5)))
    self.assertTrue(s.local_ray.direction.equals(Vector(0, 0, 1)))

  def test_shape_normal_at(self):
    s = TestShape()
    s.set_transform(Translation_Matrix(0, 1, 0))
    n = s.normal_at(Point(0, 1.70711, -0.70711))
    self.assertTrue(n.equals(Vector(0, 0.70711, -0.70711)))
    s = TestShape()
    m = Scaling_Matrix(1, 0.5, 1) * Rotation_Matrix(Rotation_Axis.Z, 36)
    s.set_transform(m)
    n = s.normal_at(Point(0, math.sqrt(2)/2.0, -1.0 * math.sqrt(2)/2.0))
    self.assertTrue(n.equals(Vector(0, 0.97014, -0.24254)))
