import math
import uuid

from abc import ABC, abstractmethod
from tuple import Point


class Primitive(ABC):
  def __init__(self):
    self.uid = str(uuid.uuid4())
    self.origin = Point(0, 0, 0)
    super().__init__()

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
