import math

from canvas import Color
from matrix import Scaling_Matrix
from operator import itemgetter
from primitive import Material, Sphere
from tuple import Point


class Intersection:
  def __init__(self, t, shape):
    self.t = t
    self.shape = shape

  def __eq__(self, intersection):
    return self.t == intersection.t and self.shape == intersection.shape

  def __getitem__(self, key):
    if key == 0:
      return self.t
    elif key == 1:
      return self.shape
    else:
      raise IndexError("Intersection item index must be 0 or 1")

  def prepare_computations(self, ray):
    return Computations(self, ray)

class Computations:
  def __init__(self, intersection, ray):
    self.t = intersection.t
    self.shape = intersection.shape
    self.point = ray.position(self.t)
    self.eyev = ray.direction.scalar_multiply(-1.0)
    self.normalv = self.shape.normal_at(self.point)
    if self.normalv.dot(self.eyev) < 0:
      self.inside = True
      self.normalv = self.normalv.scalar_multiply(-1.0)
    else:
      self.inside = False


class Ray:
  def __init__(self, origin, direction):
    self.origin = origin
    self.direction = direction
    self.intersections = []

  def position(self, t):
    return self.origin.add(self.direction.scalar_multiply(t))

  def intersect(self, shape):
    ray2 = self.transform(shape.transform.inverse())
    xs = shape.intersect(ray2)
    if len(xs) > 0:
      for t in xs:
        self.intersections.append(Intersection(t, shape))
      self.intersections.sort(key=itemgetter(0))

  def hit(self):
    for intersection in self.intersections:
      if intersection.t >= 0:
        return intersection
    return None

  def transform(self, matrix):
    origin = matrix * self.origin
    direction = matrix * self.direction
    return Ray(origin, direction)


class PointLight:
  def __init__(self, position, intensity):
    self.position = position
    self.intensity = intensity

  def lighting_at(self, material, point, eyev, normalv):
    effective_color = material.color.hadamard_product(self.intensity)
    lightv = self.position.subtract(point).normalize()
    ambient = effective_color.scalar_multiply(material.ambient)

    light_dot_normal = lightv.dot(normalv)
    if light_dot_normal < 0:
      diffuse = Color(0.0, 0.0, 0.0)
      specular = Color(0.0, 0.0, 0.0)
    else:
      diffuse = effective_color.scalar_multiply(material.diffuse * light_dot_normal)
      reflectv = lightv.scalar_multiply(-1.0).reflect(normalv)
      reflect_dot_eye = reflectv.dot(eyev)
      if reflect_dot_eye < 0:
        specular = Color(0.0, 0.0, 0.0)
      else:
        factor = math.pow(reflect_dot_eye, material.shininess)
        specular = self.intensity.scalar_multiply(material.specular * factor)

    return ambient.add(diffuse.add(specular))


class World:
  def __init__(self):
    self.light = None
    self.shapes = []

  def add_shape(self, shape):
    self.shapes.append(shape)

  def intersect(self, ray):
    for shape in self.shapes:
      ray.intersect(shape)
    return ray.intersections

  def shade_hit(self, comps):
    return self.light.lighting_at(comps.shape.material, comps.point,
                                  comps.eyev, comps.normalv)

  def color_at(self, ray):
    self.intersect(ray)
    hit = ray.hit()
    if hit:
      comps = hit.prepare_computations(ray)
      return self.shade_hit(comps)
    else:
      return Color(0.0, 0.0, 0.0)

  @staticmethod
  def default_world():
    w = World()
    w.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
    s1 = Sphere()
    material = Material()
    material.color = Color(0.8, 1.0, 0.6)
    material.diffuse = 0.7
    material.specular = 0.2
    s1.material = material
    s2 = Sphere()
    s2.set_transform(Scaling_Matrix(0.5, 0.5, 0.5))
    w.add_shape(s1)
    w.add_shape(s2)
    return w
