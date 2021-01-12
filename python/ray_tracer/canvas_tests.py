import unittest

from canvas import Canvas, Color

class CanvasTestCase(unittest.TestCase):

  def setUp(self):
    self.c1 = Color(0.9, 0.6, 0.75)
    self.c2 = Color(0.7, 0.1, 0.25)
    self.canvas = Canvas(10, 20)

  def test_color_init(self):
    c = Color(-0.5, 0.4, 1.7)
    self.assertEqual(c.r, -0.5)
    self.assertEqual(c.g, 0.4)
    self.assertEqual(c.b, 1.7)

  def test_color_operations(self):
    result = self.c1.add(self.c2)
    self.assertTrue(result.equals(Color(1.6, 0.7, 1.0)))
    result = self.c1.subtract(self.c2)
    self.assertTrue(result.equals(Color(0.2, 0.5, 0.5)))
    c = Color(0.2, 0.3, 0.4)
    result = c.scalar_multiply(2.0)
    self.assertTrue(result.equals(Color(0.4, 0.6, 0.8)))
    c1 = Color(1.0, 0.2, 0.4)
    c2 = Color(0.9, 1.0, 0.1)
    result = c1.hadamard_product(c2)
    self.assertTrue(result.equals(Color(0.9, 0.2, 0.04)))

  def test_canvas_init(self):
    black = Color(0.0, 0.0, 0.0)
    self.assertEqual(self.canvas.width, 10)
    self.assertEqual(self.canvas.height, 20)
    for x in range(self.canvas.width):
      for y in range(self.canvas.height):
        self.assertTrue(self.canvas.pixel_at(x, y).equals(black))

  def test_canvas_write_pixel(self):
    red = Color(1.0, 0.0, 0.0)
    self.canvas.write_pixel(2, 3, red)
    self.assertTrue(self.canvas.pixel_at(2, 3).equals(red))

  def test_canvas_to_ppm(self):
    c = Canvas(5, 3)
    c1 = Color(1.5, 0.0, 0.0)
    c2 = Color(0.0, 0.5, 0.0)
    c3 = Color(-0.5, 0.0, 1.0)
    c.write_pixel(0, 0, c1)
    c.write_pixel(2, 1, c2)
    c.write_pixel(4, 2, c3)
    ppm_name = "canvas.ppm"
    c.to_ppm(ppm_name)
    with open(ppm_name) as f:
      self.assertEqual(f.readline(), "P3\n")
      self.assertEqual(f.readline(), "5 3\n")
      self.assertEqual(f.readline(), "255\n")

  def test_canvas_to_ppm_split_lines(self):
    c = Canvas(10, 2, Color(1.0, 0.8, 0.6))
    ppm_name = "canvas.ppm"
    c.to_ppm(ppm_name)
    line1 = "255 204 153 255 204 153 255 204 153 255 204 153 255 204 153 255 204\n"
    line2 = "153 255 204 153 255 204 153 255 204 153 255 204 153\n"
    with open(ppm_name) as f:
      # skip header lines
      f.readline()
      f.readline()
      f.readline()
      # read data lines
      self.assertEqual(f.readline(), line1)
      self.assertEqual(f.readline(), line2)
      self.assertEqual(f.readline(), line1)
      self.assertEqual(f.readline(), line2)
