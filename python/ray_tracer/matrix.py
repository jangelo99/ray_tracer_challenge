import numpy as np


class Matrix:

  def __init__(self, data):
    self.data = np.array(data)

  def __getitem__(self, key):
    return self.data[key[0], key[1]]

  def __eq__(self, matrix):
    return np.array_equal(self.data, matrix.data)
