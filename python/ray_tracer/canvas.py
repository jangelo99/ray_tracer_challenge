
from utils import float_equal

MAX_COLOR_VALUE = 255
MAX_LINE_LENGTH = 70

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

  def __init__(self, width, height, c = Color(0.0, 0.0, 0.0)):
    self.width = width
    self.height = height
    self.pixels = [None] * self.height
    for i in range(self.height):
      self.pixels[i] = [c] * width

  def pixel_at(self, x, y):
    return self.pixels[y][x]

  def write_pixel(self, x, y, color):
    self.pixels[y][x] = color

  def to_ppm(self, ppm_name):
    with open(ppm_name, 'w') as f:
      # write the PPM file header
      f.write("P3\n")
      f.write("{0} {1}\n".format(self.width, self.height))
      f.write("{0}\n".format(MAX_COLOR_VALUE))
      # write the pixel data
      for y in range(self.height):
        row_str = ""
        for x in range(self.width):
          color = self.pixel_at(x, y)
          r = max(min(round(color.r * MAX_COLOR_VALUE), MAX_COLOR_VALUE), 0)
          if len(row_str) + len(str(r)) > MAX_LINE_LENGTH:
            f.write(row_str.strip() + "\n")
            row_str = str(r) + " "
          else:
            row_str += str(r) + " "
          g = max(min(round(color.g * MAX_COLOR_VALUE), MAX_COLOR_VALUE), 0)
          if len(row_str) + len(str(g)) > MAX_LINE_LENGTH:
            f.write(row_str.strip() + "\n")
            row_str = str(g) + " "
          else:
            row_str += str(g) + " "
          b = max(min(round(color.b * MAX_COLOR_VALUE), MAX_COLOR_VALUE), 0)
          if len(row_str) + len(str(b)) > MAX_LINE_LENGTH:
            f.write(row_str.strip() + "\n")
            row_str = str(b) + " "
          else:
            row_str += str(b) + " "
        # write line at end of each row
        f.write(row_str.strip() + "\n")
