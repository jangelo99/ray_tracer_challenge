import math

from canvas import Canvas, Color
from matrix import Rotation_Axis, Rotation_Matrix, Scaling_Matrix, Translation_Matrix
from ray_tracer import Camera, PointLight, World
from shape import Material, Sphere
from tuple import Point, Vector

if __name__ == '__main__':

  world = World()
  world.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))

  # create sphere objects for scene
  floor = Sphere()
  floor.transform = Scaling_Matrix(10, 0.01, 10)
  floor.material = Material()
  floor.material.color = Color(1, 0.9, 0.9)
  floor.material.specular = 0
  world.add_shape(floor)
  
  left_wall = Sphere()
  left_wall.transform = Translation_Matrix(0, 0, 5) * \
                        Rotation_Matrix(Rotation_Axis.Y, -45) * \
                        Rotation_Matrix(Rotation_Axis.X, 90) * \
                        Scaling_Matrix(10, 0.01, 10)
  left_wall.material = floor.material
  world.add_shape(left_wall)

  right_wall = Sphere()
  right_wall.transform = Translation_Matrix(0, 0, 5) * \
                         Rotation_Matrix(Rotation_Axis.Y, 45) * \
                         Rotation_Matrix(Rotation_Axis.X, 90) * \
                         Scaling_Matrix(10, 0.01, 10)
  right_wall.material = floor.material
  world.add_shape(right_wall)

  middle_s = Sphere()
  middle_s.transform = Translation_Matrix(-0.5, 1, 0.5)
  middle_s.material = Material()
  middle_s.material.color = Color(0.1, 1, 0.5)
  middle_s.material.diffuse = 0.7
  middle_s.material.specular = 0.3
  world.add_shape(middle_s)

  right_s = Sphere()
  right_s.transform = Translation_Matrix(1.5, 0.5, -0.5) * Scaling_Matrix(0.5, 0.5, 0.5)
  right_s.material = Material()
  right_s.material.color = Color(0.5, 1, 0.1)
  right_s.material.diffuse = 0.7
  right_s.material.specular = 0.3
  world.add_shape(right_s)

  left_s = Sphere()
  left_s.transform = Translation_Matrix(-1.5, 0.33, -0.75) * Scaling_Matrix(0.33, 0.33, 0.33)
  left_s.material = Material()
  left_s.material.color = Color(1, 0.8, 0.1)
  left_s.material.diffuse = 0.7
  left_s.material.specular = 0.3
  world.add_shape(left_s)

  # add a camera and render the scene
  camera = Camera(300, 200, math.pi / 3.0)
  from_p = Point(0, 1.5, -5)
  to_p = Point(0, 1, 0)
  up = Vector(0, 1, 0)
  camera.transform = world.view_transform(from_p, to_p, up)
  print("\nRendering scene to canvas...")
  canvas = camera.render(world)
  print("\nWriting canvas to PPM file...")
  canvas.to_ppm("canvas.ppm")
