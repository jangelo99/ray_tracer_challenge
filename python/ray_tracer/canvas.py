
from utils import EPSILON, float_equal


class Color:

  def __init__(self, red, green, blue):
    self.r = red
    self.g = green
    self.b = blue

  def equals(self, color):
    if float_equal(self.r, color.r) and float_equal(self.g, color.g) \
    and float_equal(self.b, color.b):
      return True
    else:
      return False

  def add(self, color):
    return Color(self.r + color.r, self.g + color.g, self.b + color.b)

  def subtract(self, color):
    return Color(self.r - color.r, self.g - color.g, self.b - color.b)

  def scalar_multiply(self, scalar):
    return Color(self.r * scalar, self.g * scalar, self.b * scalar)

  def hadamard_product(self, color):
    return Color(self.r * color.r, self.g * color.g, self.b * color.b)

