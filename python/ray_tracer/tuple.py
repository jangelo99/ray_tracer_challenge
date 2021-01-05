
from abc import ABC, abstractmethod

EPSILON = 0.00001

def float_equal(a, b):
  if abs(a - b) < EPSILON:
    return True
  else:
    return False

class Tuple(ABC):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.w = 1.0
    super().__init__()
    
  def equals(self, tup):
    if float_equal(self.x, tup.x) and float_equal(self.y, tup.y) \
    and float_equal(self.z, tup.z) and float_equal(self.w, tup.w):
      return True
    else:
      return False

  @abstractmethod
  def is_point(self):
    pass

  @abstractmethod
  def is_vector(self):
    pass


class Point(Tuple):
  def __init__(self, x, y, z):
    super().__init__(x, y, z)
    self.w = 1.0

  def is_point(self):
    return True

  def is_vector(self):
    return False


class Vector(Tuple):
  def __init__(self, x, y, z):
    super().__init__(x, y, z)
    self.w = 0.0

  def is_point(self):
    return False

  def is_vector(self):
    return True

