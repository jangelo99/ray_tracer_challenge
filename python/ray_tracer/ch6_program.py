from canvas import Canvas, Color
from matrix import Rotation_Axis, Rotation_Matrix, Scaling_Matrix, Shearing_Matrix
from ray_tracer import PointLight, Ray
from shape import Material, Sphere
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
  material = Material()
  material.color = Color(1, 0.2, 1)
  shape.material = material

#  shape.set_transform(Scaling_Matrix(1, 0.5, 1))
#  shape.set_transform(Scaling_Matrix(0.5, 1, 1))
#  shape.set_transform(Rotation_Matrix(Rotation_Axis.Z, 45) * Scaling_Matrix(0.5, 1, 1))
#  shape.set_transform(Shearing_Matrix(1, 0, 0, 0, 0, 0) * Scaling_Matrix(0.5, 1, 1))

  light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))

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
        point = ray.position(hit.t)
        normal = hit.shape.normal_at(point)
        eye = ray.direction.scalar_multiply(-1.0)
        color = light.lighting_at(hit.shape.material, point, eye, normal)
        canvas.write_pixel(x, y, color)

  print("Writing canvas to PPM file...")
  canvas.to_ppm("canvas.ppm")
