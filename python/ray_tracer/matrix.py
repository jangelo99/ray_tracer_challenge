import math
import numpy as np

from enum import Enum
from tuple import Tuple, Point, Vector
from utils import EPSILON


class Matrix:

  def __init__(self, data):
    self.data = np.array(data)

  def __getitem__(self, key):
    return self.data[key[0], key[1]]

  def __setitem__(self, key, value):
    self.data[key[0], key[1]] = value

  def __eq__(self, matrix):
    return np.allclose(self.data, matrix.data, atol=EPSILON, rtol=0.0)

  def __mul__(self, other):
    if isinstance(other, Matrix):
      return Matrix(np.matmul(self.data, other.data))
    elif isinstance(other, Tuple):
      b = np.array([other.x, other.y, other.z, other.w])
      result = np.matmul(self.data, b)
      if other.w == 1:
        return Point(result[0], result[1], result[2])
      else:
        return Vector(result[0], result[1], result[2])

  def transpose(self):
    return Matrix(self.data.transpose())

  def determinant(self):
    return round(np.linalg.det(self.data), 5)

  def inverse(self):
    return Matrix(np.linalg.inv(self.data))


class Identity_Matrix(Matrix):

  def __init__(self, n):
    self.data = np.identity(n)


class Translation_Matrix(Identity_Matrix):

  def __init__(self, x, y, z):
    super().__init__(4)
    self[0, 3] = x
    self[1, 3] = y
    self[2, 3] = z


class Scaling_Matrix(Identity_Matrix):

  def __init__(self, x, y, z):
    super().__init__(4)
    self[0, 0] = x
    self[1, 1] = y
    self[2, 2] = z


class Rotation_Axis(Enum):
  X = 1
  Y = 2
  Z = 3

class Rotation_Matrix(Identity_Matrix):

  def __init__(self, axis, degrees):
    super().__init__(4)
    rads = math.radians(degrees)
    if axis == Rotation_Axis.X:
      self[1, 1] = math.cos(rads)
      self[1, 2] = -1.0 * math.sin(rads)
      self[2, 1] = math.sin(rads)
      self[2, 2] = math.cos(rads)
    elif axis == Rotation_Axis.Y:
      self[0, 0] = math.cos(rads)
      self[0, 2] = math.sin(rads)
      self[2, 0] = -1.0 * math.sin(rads)
      self[2, 2] = math.cos(rads)
    elif axis == Rotation_Axis.Z:
      self[0, 0] = math.cos(rads)
      self[0, 1] = -1.0 * math.sin(rads)
      self[1, 0] = math.sin(rads)
      self[1, 1] = math.cos(rads)
    else:
      raise TypeError("Invalid Rotation_Axis for rotation matrix")
