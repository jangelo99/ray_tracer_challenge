import math
import uuid

from abc import ABC, abstractmethod
from matrix import Identity_Matrix
from tuple import Point


class Primitive(ABC):
  def __init__(self):
    self.uid = str(uuid.uuid4())
    self.origin = Point(0, 0, 0)
    self.transform = Identity_Matrix(4)
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


class Sphere(Primitive):

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
