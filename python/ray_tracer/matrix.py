import numpy as np

from tuple import Tuple, Point, Vector


class Matrix:

  def __init__(self, data):
    self.data = np.array(data)

  def __getitem__(self, key):
    return self.data[key[0], key[1]]

  def __eq__(self, matrix):
    return np.array_equal(self.data, matrix.data)

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
