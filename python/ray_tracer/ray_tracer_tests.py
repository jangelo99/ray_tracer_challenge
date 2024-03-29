import math
import unittest

from canvas import Color
from matrix import Matrix, Identity_Matrix, Rotation_Axis, Rotation_Matrix, Scaling_Matrix, Translation_Matrix
from pattern import TestPattern
from ray_tracer import Camera, Intersection, PointLight, Ray, World
from shape import Material, Plane, Sphere
from tuple import Point, Vector
from utils import float_equal, EPSILON

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
    # test when in_shadow is true
    eyev = Vector(0, 0, -1)
    normalv = Vector(0, 0, -1)
    light = PointLight(Point(0, 0, -10), intensity)
    in_shadow = True
    result = light.lighting_at(m, position, eyev, normalv, in_shadow)
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
    # test case for over_point attribute
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere()
    shape.transform = Translation_Matrix(0, 0, 1)
    i = Intersection(5, shape)
    comps = i.prepare_computations(r)
    self.assertTrue(comps.over_point.z < -1.0 * (EPSILON / 2.0))
    # test case for under_point attribute
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    shape = Sphere.glass_sphere()
    shape.transform = Translation_Matrix(0, 0, 1)
    i = Intersection(5, shape)
    comps = i.prepare_computations(r)
    self.assertTrue(comps.under_point.z > EPSILON / 2.0)

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
    # test case for shadowed point
    w = World()
    w.light = PointLight(Point(0, 0, -10), Color(1, 1, 1))
    s1 = Sphere()
    w.add_shape(s1)
    s2 = Sphere()
    s2.transform = Translation_Matrix(0, 0, 10)
    w.add_shape(s2)
    r = Ray(Point(0, 0, 5), Vector(0, 1, 0))
    i = Intersection(4, s2)
    comps = i.prepare_computations(r)
    c = w.shade_hit(comps)
    self.assertTrue(c.equals(Color(0.1, 0.1, 0.1)))

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

  def test_camera_render(self):
    w = World.default_world()
    c = Camera(11, 11, math.pi / 2.0)
    from_p = Point(0, 0, -5)
    to_p = Point(0, 0, 0)
    up = Vector(0, 1, 0)
    c.transform = w.view_transform(from_p, to_p, up)
    image = c.render(w)
    self.assertTrue(image.pixel_at(5, 5).equals(Color(0.38066, 0.47583, 0.2855)))

  def test_world_is_shadowed(self):
    w = World.default_world()
    p = Point(0, 10, 0)
    self.assertEqual(w.is_shadowed(p), False)
    p = Point(10, -10, 10)
    self.assertEqual(w.is_shadowed(p), True)
    p = Point(-20, 20, -20)
    self.assertEqual(w.is_shadowed(p), False)
    p = Point(-2, 2, -2)
    self.assertEqual(w.is_shadowed(p), False)

  def test_reflection_vector(self):
    shape = Plane()
    r = Ray(Point(0, 1, -1), Vector(0, -math.sqrt(2.0)/2.0, math.sqrt(2.0)/2.0))
    i = Intersection(math.sqrt(2.0), shape)
    comps = i.prepare_computations(r)
    self.assertTrue(comps.reflectv.equals(Vector(0, math.sqrt(2.0)/2.0, math.sqrt(2.0)/2.0)))

  def test_reflected_color(self):
    # reflected color for non-reflective material
    w = World.default_world()
    r = Ray(Point(0, 0, 0), Vector(0, 0, 1))
    shape = w.shapes[1]
    shape.material.ambient = 1
    i = Intersection(1, shape)
    comps = i.prepare_computations(r)
    color = w.reflected_color(comps, 4)
    self.assertTrue(color.equals(Color(0, 0, 0)))
    # reflected color for reflective material
    w = World.default_world()
    shape = Plane()
    shape.material.reflective = 0.5
    shape.transform = Translation_Matrix(0, -1, 0)
    w.add_shape(shape)
    r = Ray(Point(0, 0, -3), Vector(0, -math.sqrt(2.0)/2.0, math.sqrt(2.0)/2.0))
    i = Intersection(math.sqrt(2.0), shape)
    comps = i.prepare_computations(r)
    color = w.reflected_color(comps, 4)
    self.assertTrue(color.equals(Color(0.19033, 0.23792, 0.14275)))
    # call shade_hit directly
    color = w.shade_hit(comps)
    self.assertTrue(color.equals(Color(0.87676, 0.92434, 0.82917)))

  def test_find_n1_n2(self):
    A = Sphere.glass_sphere()
    A.set_transform(Scaling_Matrix(2, 2, 2))
    A.material.refractive_index = 1.5
    B = Sphere.glass_sphere()
    B.set_transform(Translation_Matrix(0, 0, -0.25))
    B.material.refractive_index = 2.0
    C = Sphere.glass_sphere()
    C.set_transform(Translation_Matrix(0, 0, 0.25))
    C.material.refractive_index = 2.5
    r = Ray(Point(0, 0, -4), Vector(0, 0, 1))
    xs = [Intersection(2, A), Intersection(2.75, B), Intersection(3.25, C), Intersection(4.75, B), Intersection(5.25, C), Intersection(6, A)]
    r.intersections = xs
    comps = xs[0].prepare_computations(r)
    self.assertEqual(comps.n1, 1.0)
    self.assertEqual(comps.n2, 1.5)
    comps = xs[1].prepare_computations(r)
    self.assertEqual(comps.n1, 1.5)
    self.assertEqual(comps.n2, 2.0)
    comps = xs[2].prepare_computations(r)
    self.assertEqual(comps.n1, 2.0)
    self.assertEqual(comps.n2, 2.5)
    comps = xs[3].prepare_computations(r)
    self.assertEqual(comps.n1, 2.5)
    self.assertEqual(comps.n2, 2.5)
    comps = xs[4].prepare_computations(r)
    self.assertEqual(comps.n1, 2.5)
    self.assertEqual(comps.n2, 1.5)
    comps = xs[5].prepare_computations(r)
    self.assertEqual(comps.n1, 1.5)
    self.assertEqual(comps.n2, 1.0)

  def test_refracted_color(self):
    # refracted color for an opaque material
    w = World.default_world()
    shape = w.shapes[0]
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = [Intersection(4, shape), Intersection(6, shape)]
    r.intersections = xs
    comps = xs[0].prepare_computations(r)
    color = w.refracted_color(comps, 5)
    self.assertTrue(color.equals(Color(0, 0, 0)))
    # refracted color at max recursive depth
    w = World.default_world()
    shape = w.shapes[0]
    shape.material.transparency = 1.0
    shape.material.refractive_index = 1.5
    r = Ray(Point(0, 0, -5), Vector(0, 0, 1))
    xs = [Intersection(4, shape), Intersection(6, shape)]
    r.intersections = xs
    comps = xs[0].prepare_computations(r)
    color = w.refracted_color(comps, 0)
    self.assertTrue(color.equals(Color(0, 0, 0)))
    # refracted color under total internal reflection
    w = World.default_world()
    shape = w.shapes[0]
    shape.material.transparency = 1.0
    shape.material.refractive_index = 1.5
    r = Ray(Point(0, 0, math.sqrt(2.0)/2.0), Vector(0, 1, 0))
    xs = [Intersection(-1.0 * math.sqrt(2.0)/2.0, shape), Intersection(math.sqrt(2.0)/2.0, shape)]
    r.intersections = xs
    comps = xs[1].prepare_computations(r)
    color = w.refracted_color(comps, 5)
    self.assertTrue(color.equals(Color(0, 0, 0)))
    # refracted color in all other cases
    w = World.default_world()
    A = w.shapes[0]
    A.material.ambient = 1.0
    A.material.pattern = TestPattern()
    B = w.shapes[1]
    B.material.transparency = 1.0
    B.material.refractive_index = 1.5
    r = Ray(Point(0, 0, 0.1), Vector(0, 1, 0))
    xs = [Intersection(-0.9899, A), Intersection(-0.4899, B), Intersection(0.4899, B), Intersection(0.9899, A)]
    r.intersections = xs
    comps = xs[2].prepare_computations(r)
    color = w.refracted_color(comps, 5)
    self.assertTrue(color.equals(Color(0, 0.99888, 0.04722)))
    # call shade_hit directly
    w = World.default_world()
    floor = Plane()
    floor.transform = Translation_Matrix(0, -1, 0)
    floor.material.reflective = 0.5
    floor.material.transparency = 0.5
    floor.material.refractive_index = 1.5
    w.add_shape(floor)
    ball = Sphere()
    ball.material.color = Color(1, 0, 0)
    ball.material.ambient = 0.5
    ball.transform = Translation_Matrix(0, -3.5, -0.5)
    w.add_shape(ball)
    r = Ray(Point(0, 0, -3), Vector(0, -1.0*math.sqrt(2.0)/2.0, math.sqrt(2.0)/2.0))
    xs = [Intersection(math.sqrt(2.0), floor)]
    r.intersections = xs
    comps = xs[0].prepare_computations(r)
    color = w.shade_hit(comps, 5)
    self.assertTrue(color.equals(Color(0.93391, 0.69643, 0.69243)))

  def test_comps_schlick(self):
    shape = Sphere.glass_sphere()
    r = Ray(Point(0, 0, math.sqrt(2.0)/2.0), Vector(0, 1, 0))
    xs = [Intersection(-1.0 * math.sqrt(2.0)/2.0, shape), Intersection(math.sqrt(2.0)/2.0, shape)]
    r.intersections = xs
    comps = xs[1].prepare_computations(r)
    reflectance = comps.schlick()
    self.assertEqual(reflectance, 1.0)
    r = Ray(Point(0, 0, 0), Vector(0, 1, 0))
    xs = [Intersection(-1, shape), Intersection(1, shape)]
    r.intersections = xs
    comps = xs[1].prepare_computations(r)
    reflectance = comps.schlick()
    self.assertTrue(float_equal(reflectance, 0.04))
    r = Ray(Point(0, 0.99, -2), Vector(0, 0, 1))
    xs = [Intersection(1.8589, shape)]
    r.intersections = xs
    comps = xs[0].prepare_computations(r)
    reflectance = comps.schlick()
    self.assertTrue(float_equal(reflectance, 0.48873))
