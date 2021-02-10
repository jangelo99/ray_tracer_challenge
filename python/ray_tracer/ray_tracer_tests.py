import math
import unittest

from canvas import Color
from matrix import Matrix, Identity_Matrix, Rotation_Axis, Rotation_Matrix, Scaling_Matrix, Translation_Matrix
from primitive import Material, Sphere
from ray_tracer import Camera, Intersection, PointLight, Ray, World
from tuple import Point, Vector
from utils import float_equal

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

  def test_default_world(self):
    w = World.default_world()
    self.assertTrue(w.light.intensity.equals(Color(1, 1, 1)))
    self.assertTrue(w.light.position.equals(Point(-10, 10, -10)))
    self.assertEqual(len(w.shapes), 2)
    s1 = w.shapes[0]
    self.assertTrue(s1.material.color.equals(Color(0.8, 1.0, 0.6)))
    self.assertEqual(s1.material.diffuse, 0.7)
    self.assertEqual(s1.material.specular, 0.2)
    s2 = w.shapes[1]
    self.assertEqual(s2.transform, Scaling_Matrix(0.5, 0.5, 0.5))

  def test_world_intersect(self):
    w = World.default_world()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = w.intersect(r)
    self.assertEqual(len(xs), 4)
    self.assertEqual(xs[0].t, 4)
    self.assertEqual(xs[1].t, 4.5)
    self.assertEqual(xs[2].t, 5.5)
    self.assertEqual(xs[3].t, 6)

  def test_prepare_computations(self):
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(4, shape)
    comps = i.prepare_computations(r)
    self.assertEqual(comps.t, i.t)
    self.assertEqual(comps.shape, i.shape)
    self.assertTrue(comps.point.equals(Point(0, 0, -1)))
    self.assertTrue(comps.eyev.equals(Vector(0, 0, -1)))
    self.assertTrue(comps.normalv.equals(Vector(0, 0, -1)))
    self.assertTrue(comps.inside == False)
    # test case where hit occurs on inside of shape
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = Sphere()
    i = Intersection(1, shape)
    comps = i.prepare_computations(r)
    self.assertTrue(comps.point.equals(Point(0, 0, 1)))
    self.assertTrue(comps.eyev.equals(Vector(0, 0, -1)))
    self.assertTrue(comps.normalv.equals(Vector(0, 0, -1)))
    self.assertTrue(comps.inside == True)

  def test_world_shade_hit(self):
    w = World.default_world()
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = w.shapes[0]
    i = Intersection(4, shape)
    comps = i.prepare_computations(r)
    c = w.shade_hit(comps)
    self.assertTrue(c.equals(Color(0.38066, 0.47583, 0.2855)))
    # test case where hit occurs on inside of shape
    w = World.default_world()
    w.light = PointLight(Point(0, 0.25, 0), Color(1, 1, 1))
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = w.shapes[1]
    i = Intersection(0.5, shape)
    comps = i.prepare_computations(r)
    c = w.shade_hit(comps)
    self.assertTrue(c.equals(Color(0.90498, 0.90498, 0.90498)))

  def test_world_color_at(self):
    # color when ray misses
    w = World.default_world()
    r = Ray(Point(0, 0, -5), Vector(0, 1, 0))
    c = w.color_at(r)
    self.assertTrue(c.equals(Color(0, 0, 0)))
    # color when ray hits
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    c = w.color_at(r)
    self.assertTrue(c.equals(Color(0.38066, 0.47583, 0.2855)))
    # color with an intersection behind the ray
    outer = w.shapes[0]
    outer.material.ambient = 1
    inner = w.shapes[1]
    inner.material.ambient = 1
    r = Ray(Point(0, 0, 0.75), Vector(0, 0, -1))
    c = w.color_at(r)
    self.assertTrue(c.equals(inner.material.color))

  def test_world_view_transform(self):
    w = World.default_world()
    from_p = Point(0, 0, 0)
    to_p = Point(0, 0, -1)
    up = Vector(0, 1, 0)
    t = w.view_transform(from_p, to_p, up)
    self.assertEqual(t, Identity_Matrix(4))
    from_p = Point(0, 0, 0)
    to_p = Point(0, 0, 1)
    up = Vector(0, 1, 0)
    t = w.view_transform(from_p, to_p, up)
    self.assertEqual(t, Scaling_Matrix(-1, 1, -1))
    from_p = Point(0, 0, 8)
    to_p = Point(0, 0, 0)
    up = Vector(0, 1, 0)
    t = w.view_transform(from_p, to_p, up)
    self.assertEqual(t, Translation_Matrix(0, 0, -8))
    from_p = Point(1, 3, 2)
    to_p = Point(4, -2, 8)
    up = Vector(1, 1, 0)
    t = w.view_transform(from_p, to_p, up)
    self.assertEqual(t, Matrix([[-0.50709, 0.50709, 0.67612, -2.36643],
                                [0.76772, 0.60609, 0.12122, -2.82843],
                                [-0.35857, 0.59761, -0.71714, 0.00000],
                                [0.00000, 0.00000, 0.00000, 1.00000]]))

  def test_camera_pixel_size(self):
    c1 = Camera(200, 125, math.pi / 2.0)
    self.assertTrue(float_equal(c1.pixel_size, 0.01))
    c2 = Camera(125, 200, math.pi / 2.0)
    self.assertTrue(float_equal(c2.pixel_size, 0.01))

  def test_camera_ray_for_pixel(self):
    c = Camera(201, 101, math.pi / 2.0)
    r = c.ray_for_pixel(100, 50)
    self.assertTrue(r.origin.equals(Point(0, 0, 0)))
    self.assertTrue(r.direction.equals(Vector(0, 0, -1)))
    r = c.ray_for_pixel(0, 0)
    self.assertTrue(r.origin.equals(Point(0, 0, 0)))
    self.assertTrue(r.direction.equals(Vector(0.66519, 0.33259, -0.66851)))
    c = Camera(201, 101, math.pi / 2.0)
    c.transform = Rotation_Matrix(Rotation_Axis.Y, 45) * Translation_Matrix(0, -2, 5)
    r = c.ray_for_pixel(100, 50)
    self.assertTrue(r.origin.equals(Point(0, 2, -5)))
    self.assertTrue(r.direction.equals(Vector(math.sqrt(2.0)/2.0, 0, -math.sqrt(2.0)/2.0)))
