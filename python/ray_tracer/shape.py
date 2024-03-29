import math
import uuid

from abc import ABC, abstractmethod
from canvas import Color
from matrix import Identity_Matrix
from tuple import Point, Vector
from utils import EPSILON, float_equal


class Material:
  def __init__(self):
    self.color = Color(1.0, 1.0, 1.0)
    self.pattern = None
    self.ambient = 0.1
    self.diffuse = 0.9
    self.specular = 0.9
    self.shininess = 200.0
    self.reflective = 0.0
    self.transparency = 0.0
    self.refractive_index = 1.0

  def equals(self, material):
    if self.color.equals(material.color) \
    and self.pattern == material.pattern \
    and float_equal(self.ambient, material.ambient) \
    and float_equal(self.diffuse, material.diffuse) \
    and float_equal(self.specular, material.specular) \
    and float_equal(self.shininess, material.shininess) \
    and float_equal(self.reflective, material.reflective) \
    and float_equal(self.transparency, material.transparency) \
    and float_equal(self.refractive_index, material.refractive_index):
      return True
    else:
      return False


class Shape(ABC):
  def __init__(self):
    self.uid = str(uuid.uuid4())
    self.origin = Point(0, 0, 0)
    self.transform = Identity_Matrix(4)
    self.material = Material()
    self.local_ray = None
    super().__init__()

  def set_transform(self, transform):
    self.transform = transform

  def normal_at(self, world_point):
    inv_transform = self.transform.inverse()
    object_point = inv_transform * world_point
    object_normal = object_point.subtract(self.origin)
    world_normal = inv_transform.transpose() * object_normal
    world_normal.w = 0
    return world_normal.normalize()

  def intersect(self, ray):
    self.local_ray = ray.transform(self.transform.inverse())
    return self.local_intersect(self.local_ray)

  @abstractmethod
  def local_intersect(self, ray):
    pass

class TestShape(Shape):

  def local_intersect(self, ray):
    return []


class Sphere(Shape):

  def local_intersect(self, ray):
    sphere_to_ray = ray.origin.subtract(self.origin)
    a = ray.direction.dot(ray.direction)
    b = 2.0 * ray.direction.dot(sphere_to_ray)
    c = sphere_to_ray.dot(sphere_to_ray) - 1.0
    discrim = (b * b) - (4 * a * c)
    if discrim < 0:
      return []
    else:
      t1 = (-1.0 * b - math.sqrt(discrim)) / (2 * a)
      t2 = (-1.0 * b + math.sqrt(discrim)) / (2 * a)
      return [t1, t2]

  @staticmethod
  def glass_sphere():
    s = Sphere()
    s.material.transparency = 1.0
    s.material.refractive_index = 1.5
    return s


class Plane(Shape):

  def __init__(self):
    super().__init__()
    # all points on the plane have the same object normal
    self.object_normal = Vector(0, 1, 0)

  def normal_at(self, world_point):
    inv_transform = self.transform.inverse()
    world_normal = inv_transform.transpose() * self.object_normal
    world_normal.w = 0
    return world_normal.normalize()

  def local_intersect(self, ray):
    if abs(ray.direction.y) < EPSILON:
      return []
    else:
      t = (-1.0 * ray.origin.y) / ray.direction.y
      return [t]
