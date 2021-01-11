
import math

from abc import ABC, abstractmethod
from utils import float_equal


class TupleException(Exception):
  pass

  
class InvalidOperationError(TupleException):
  pass


class Tuple(ABC):
  def __init__(self, x, y, z, w):
    self.x = x
    self.y = y
    self.z = z
    self.w = w
    super().__init__()
    
  def equals(self, tup):
    if float_equal(self.x, tup.x) and float_equal(self.y, tup.y) \
    and float_equal(self.z, tup.z) and float_equal(self.w, tup.w):
      return True
    else:
      return False

  def is_point(self):
    return self.w == 1.0

  def is_vector(self):
    return self.w == 0.0

  @abstractmethod
  def add(self, tup):
    pass

  @abstractmethod
  def subtract(self, tup):
    pass


class Point(Tuple):
  def __init__(self, x, y, z):
    super().__init__(x, y, z, 1.0)
    
  def add(self, tup):
    if tup.is_point():
      raise InvalidOperationError("Can't add a Point to another Point")
    else:
      return Point(self.x + tup.x, self.y + tup.y, self.z + tup.z)
      
  def subtract(self, tup):
    if tup.is_point():
      return Vector(self.x - tup.x, self.y - tup.y, self.z - tup.z)
    else:
      return Point(self.x - tup.x, self.y - tup.y, self.z - tup.z)


class Vector(Tuple):
  def __init__(self, x, y, z):
    super().__init__(x, y, z, 0.0)
    
  def add(self, tup):
    if tup.is_point():
      return Point(self.x + tup.x, self.y + tup.y, self.z + tup.z)
    else:
      return Vector(self.x + tup.x, self.y + tup.y, self.z + tup.z)

  def subtract(self, tup):
    if tup.is_point():
      raise InvalidOperationError("Can't subtract a Point from a Vector")
    else:
      return Vector(self.x - tup.x, self.y - tup.y, self.z - tup.z)

  def scalar_multiply(self, scalar):
    return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

  def scalar_divide(self, scalar):
    return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

  def negate(self):
    return self.scalar_multiply(-1.0)

  def magnitude(self):
    return math.sqrt(self.x**2 + self.y**2 + self.z**2)

  def normalize(self):
    if float_equal(self.magnitude(), 0.0):
      raise InvalidOperationError("Can't normalize a Vector with zero magnitude")
    else:
      return self.scalar_divide(self.magnitude())

  def dot(self, vec):
    return (self.x * vec.x) + (self.y * vec.y) + (self.z * vec.z)

  def cross(self, vec):
    x = (self.y * vec.z) - (self.z * vec.y)
    y = (self.z * vec.x) - (self.x * vec.z)
    z = (self.x * vec.y) - (self.y * vec.x)
    return Vector(x, y, z)
