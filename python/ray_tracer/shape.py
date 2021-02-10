import math
import uuid

from abc import ABC, abstractmethod
from canvas import Color
from matrix import Identity_Matrix
from tuple import Point
from utils import float_equal


class Material:
  def __init__(self):
    self.color = Color(1.0, 1.0, 1.0)
    self.ambient = 0.1
    self.diffuse = 0.9
    self.specular = 0.9
    self.shininess = 200.0

  def equals(self, material):
    if self.color.equals(material.color) \
    and float_equal(self.ambient, material.ambient) \
    and float_equal(self.diffuse, material.diffuse) \
    and float_equal(self.specular, material.specular) \
    and float_equal(self.shininess, material.shininess):
      return True
    else:
      return False


class Shape(ABC):
  def __init__(self):
    self.uid = str(uuid.uuid4())
    self.origin = Point(0, 0, 0)
    self.transform = Identity_Matrix(4)
    self.material = Material()
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

  @abstractmethod
  def intersect(self, ray):
    pass


class Sphere(Shape):

  def intersect(self, ray):
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
