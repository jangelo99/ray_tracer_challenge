import math

from abc import ABC, abstractmethod
from canvas import Color
from matrix import Identity_Matrix

class Pattern(ABC):
  def __init__(self):
    self.transform = Identity_Matrix(4)
    super().__init__()

  def set_transform(self, transform):
    self.transform = transform
  
  def pattern_at_shape(self, shape, world_point):
    object_point = shape.transform.inverse() * world_point
    pattern_point = self.transform.inverse() * object_point
    return self.pattern_at(pattern_point)
  
  @abstractmethod
  def pattern_at(self, point):
    pass

class TestPattern(Pattern):

  def pattern_at(self, point):
    return Color(point.x, point.y, point.z)


class StripePattern(Pattern):

  def __init__(self, ca, cb):
    super().__init__()
    self.ca = ca
    self.cb = cb

  def pattern_at(self, point):
    if math.floor(point.x) % 2 == 0:
      return self.ca
    else:
      return self.cb


class GradientPattern(Pattern):

  def __init__(self, ca, cb):
    super().__init__()
    self.ca = ca
    self.cb = cb

  def pattern_at(self, point):
    distance = self.cb.subtract(self.ca)
    fraction = point.x - math.floor(point.x)
    return self.ca.add(distance.scalar_multiply(fraction))
