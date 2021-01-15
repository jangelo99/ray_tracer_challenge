import numpy as np

from tuple import Tuple, Point, Vector
from utils import EPSILON


class Matrix:

  def __init__(self, data):
    self.data = np.array(data)

  def __getitem__(self, key):
    return self.data[key[0], key[1]]

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
