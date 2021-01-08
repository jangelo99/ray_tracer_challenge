
from abc import ABC, abstractmethod

EPSILON = 0.00001

def float_equal(a, b):
  if abs(a - b) < EPSILON:
    return True
  else:
    return False

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
