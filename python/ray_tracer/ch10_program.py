import math

from canvas import Canvas, Color
from matrix import Rotation_Axis, Rotation_Matrix, Scaling_Matrix, Translation_Matrix
from pattern import CheckerPattern, GradientPattern, RingPattern, StripePattern
from ray_tracer import Camera, PointLight, World
from shape import Material, Plane, Sphere
from tuple import Point, Vector

if __name__ == '__main__':

  world = World()
  world.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))

  # create plane objects for floor and wall
  floor = Plane()
  floor.material = Material()
  floor.material.specular = 0
#  floor.material.color = Color(1, 0.9, 0.9)
  floor.material.pattern = RingPattern(Color(0.2, 0, 0), Color(1, 1, 1))
#  floor.material.pattern = CheckerPattern(Color(1, 1, 1), Color(0, 0, 0))
  world.add_shape(floor)
  
  wall = Plane()
  wall.transform = Translation_Matrix(0, 0, 5) * Rotation_Matrix(Rotation_Axis.X, 90)
  wall.material = Material()
  wall.material.specular = 0
  wall.material.pattern = StripePattern(Color(1, 0.9, 0.9), Color(0, 0, 0))
  world.add_shape(wall)

  # create sphere objects for scene
  middle_s = Sphere()
  middle_s.transform = Translation_Matrix(-0.5, 1, 0.5)
  middle_s.material = Material()
#  middle_s.material.color = Color(0.1, 1, 0.5)
  check_pattern = CheckerPattern(Color(1, 1, 1), Color(0.1, 1, 0.5))
  check_pattern.transform = Scaling_Matrix(0.4, 0.4, 0.4)
  middle_s.material.pattern = check_pattern
#  middle_s.material.pattern = RingPattern(Color(0.1, 1, 0.5), Color(1, 1, 1))
  middle_s.material.diffuse = 0.7
  middle_s.material.specular = 0.3
  world.add_shape(middle_s)

  right_s = Sphere()
  right_s.transform = Translation_Matrix(1.5, 0.5, -0.5) * Scaling_Matrix(0.5, 0.5, 0.5)
  right_s.material = Material()
#  right_s.material.color = Color(0.5, 1, 0.1)
  grad_pattern = GradientPattern(Color(1, 0.1, 0.1), Color(0.5, 1, 0.1))
  grad_pattern.transform = Rotation_Matrix(Rotation_Axis.Y, 115) * Scaling_Matrix(1.5, 1.5, 1.5)
  right_s.material.pattern = grad_pattern
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
  camera = Camera(200, 100, math.pi / 3.0)
  from_p = Point(0, 1.5, -5)
  to_p = Point(0, 1, 0)
  up = Vector(0, 1, 0)
  camera.transform = world.view_transform(from_p, to_p, up)
  print("\nRendering scene to canvas...")
  canvas = camera.render(world)
  print("\nWriting canvas to PPM file...")
  canvas.to_ppm("canvas.ppm")
