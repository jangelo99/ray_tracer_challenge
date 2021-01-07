
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
  def add(self, tup):
    pass

  @abstractmethod
  def subtract(self, tup):
    pass

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

  def is_point(self):
    return True

  def is_vector(self):
    return False


class Vector(Tuple):
  def __init__(self, x, y, z):
    super().__init__(x, y, z)
    self.w = 0.0
    
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

  def is_point(self):
    return False

  def is_vector(self):
    return True

