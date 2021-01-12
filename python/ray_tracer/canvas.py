
from utils import float_equal


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


class Canvas:

  def __init__(self, width, height):
    self.width = width
    self.height = height
    c = Color(0.0, 0.0, 0.0)
    self.pixels = [None] * self.height
    for i in range(self.height):
      self.pixels[i] = [c] * width

  def pixel_at(self, x, y):
    return self.pixels[y][x]

  def write_pixel(self, x, y, color):
    self.pixels[y][x] = color
