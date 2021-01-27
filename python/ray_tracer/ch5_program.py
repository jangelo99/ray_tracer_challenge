from canvas import Canvas, Color
from primitive import Sphere
from ray_tracer import Ray
from tuple import Point

if __name__ == '__main__':

  ray_origin = Point(0, 0, -5)

  wall_z = 10
  wall_size = 7.0
  half = wall_size / 2.0

  canvas_pixels = 100
  pixel_size = wall_size / canvas_pixels

  canvas = Canvas(canvas_pixels, canvas_pixels)
  red = Color(1, 0, 0)
  shape = Sphere()

  print("Creating canvas...")
  for y in range(canvas_pixels):
    world_y = half - pixel_size * y
    for x in range(canvas_pixels):
      world_x = -1.0 * half + pixel_size * x
      position = Point(world_x, world_y, wall_z)
      ray = Ray(ray_origin, position.subtract(ray_origin).normalize())
      ray.intersect(shape)
      hit = ray.hit()
      if hit:
        canvas.write_pixel(x, y, red)

  print("Writing canvas to PPM file...")
  canvas.to_ppm("canvas.ppm")
