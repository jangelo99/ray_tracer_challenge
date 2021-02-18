import math

from canvas import Canvas, Color
from matrix import Matrix, Identity_Matrix, Scaling_Matrix, Translation_Matrix
from operator import itemgetter
from shape import Material, Sphere
from tuple import Point
from utils import EPSILON


DEFAULT_REMAINING = 4

class Intersection:
  def __init__(self, t, shape):
    self.t = t
    self.shape = shape

  def __eq__(self, intersection):
    return self.t == intersection.t and self.shape == intersection.shape

  def __getitem__(self, key):
    if key == 0:
      return self.t
    elif key == 1:
      return self.shape
    else:
      raise IndexError("Intersection item index must be 0 or 1")

  def prepare_computations(self, ray):
    return Computations(self, ray)

class Computations:
  def __init__(self, intersection, ray):
    self.t = intersection.t
    self.shape = intersection.shape
    self.point = ray.position(self.t)
    self.eyev = ray.direction.scalar_multiply(-1.0)
    self.normalv = self.shape.normal_at(self.point)
    if self.normalv.dot(self.eyev) < 0:
      self.inside = True
      self.normalv = self.normalv.scalar_multiply(-1.0)
    else:
      self.inside = False
    self.over_point = self.point.add(self.normalv.scalar_multiply(EPSILON))
    self.reflectv = ray.direction.reflect(self.normalv)


class Ray:
  def __init__(self, origin, direction):
    self.origin = origin
    self.direction = direction
    self.intersections = []

  def position(self, t):
    return self.origin.add(self.direction.scalar_multiply(t))

  def intersect(self, shape):
    xs = shape.intersect(self)
    if len(xs) > 0:
      for t in xs:
        self.intersections.append(Intersection(t, shape))
      self.intersections.sort(key=itemgetter(0))

  def hit(self):
    for intersection in self.intersections:
      if intersection.t >= 0:
        return intersection
    return None

  def transform(self, matrix):
    origin = matrix * self.origin
    direction = matrix * self.direction
    return Ray(origin, direction)


class PointLight:
  def __init__(self, position, intensity):
    self.position = position
    self.intensity = intensity

  def lighting_at(self, material, point, eyev, normalv, in_shadow=False, shape=Sphere()):
    if material.pattern:
      color = material.pattern.pattern_at_shape(shape, point)
    else:
      color = material.color
    effective_color = color.hadamard_product(self.intensity)
    ambient = effective_color.scalar_multiply(material.ambient)

    if in_shadow:
      return ambient

    lightv = self.position.subtract(point).normalize()
    light_dot_normal = lightv.dot(normalv)
    if light_dot_normal < 0:
      diffuse = Color(0.0, 0.0, 0.0)
      specular = Color(0.0, 0.0, 0.0)
    else:
      diffuse = effective_color.scalar_multiply(material.diffuse * light_dot_normal)
      reflectv = lightv.scalar_multiply(-1.0).reflect(normalv)
      reflect_dot_eye = reflectv.dot(eyev)
      if reflect_dot_eye < 0:
        specular = Color(0.0, 0.0, 0.0)
      else:
        factor = math.pow(reflect_dot_eye, material.shininess)
        specular = self.intensity.scalar_multiply(material.specular * factor)

    return ambient.add(diffuse.add(specular))


class World:
  def __init__(self):
    self.light = None
    self.shapes = []

  def add_shape(self, shape):
    self.shapes.append(shape)

  def intersect(self, ray):
    for shape in self.shapes:
      ray.intersect(shape)
    return ray.intersections

  def is_shadowed(self, point):
    v = self.light.position.subtract(point)
    distance = v.magnitude()
    direction = v.normalize()
    ray = Ray(point, direction)
    self.intersect(ray)
    hit = ray.hit()
    if hit and hit.t < distance:
      return True
    else:
      return False

  def shade_hit(self, comps, remaining=DEFAULT_REMAINING):
    shadowed = self.is_shadowed(comps.over_point)
    surface = self.light.lighting_at(comps.shape.material, comps.over_point,
                                     comps.eyev, comps.normalv, shadowed, comps.shape)
    reflected = self.reflected_color(comps, remaining)
    return surface.add(reflected)

  def color_at(self, ray, remaining=DEFAULT_REMAINING):
    self.intersect(ray)
    hit = ray.hit()
    if hit:
      comps = hit.prepare_computations(ray)
      return self.shade_hit(comps, remaining)
    else:
      return Color(0.0, 0.0, 0.0)

  def view_transform(self, from_p, to_p, up):
    forward = to_p.subtract(from_p).normalize()
    upn = up.normalize()
    left = forward.cross(upn)
    true_up = left.cross(forward)
    orientation = Matrix([[left.x, left.y, left.z, 0.0],
                          [true_up.x, true_up.y, true_up.z, 0.0],
                          [-1*forward.x, -1*forward.y, -1*forward.z, 0.0],
                          [0.0, 0.0, 0.0, 1.0]])
    return orientation * Translation_Matrix(-1*from_p.x, -1*from_p.y, -1*from_p.z)

  def reflected_color(self, comps, remaining):
    if remaining <= 0 or comps.shape.material.reflective == 0:
      return Color(0, 0, 0)

    reflect_ray = Ray(comps.over_point, comps.reflectv)
    color = self.color_at(reflect_ray, remaining - 1)
    return color.scalar_multiply(comps.shape.material.reflective)

  @staticmethod
  def default_world():
    w = World()
    w.light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))
    s1 = Sphere()
    material = Material()
    material.color = Color(0.8, 1.0, 0.6)
    material.diffuse = 0.7
    material.specular = 0.2
    s1.material = material
    s2 = Sphere()
    s2.set_transform(Scaling_Matrix(0.5, 0.5, 0.5))
    w.add_shape(s1)
    w.add_shape(s2)
    return w


class Camera:
  def __init__(self, hsize, vsize, field_of_view):
    self.hsize = hsize
    self.vsize = vsize
    self.field_of_view = field_of_view
    self.transform = Identity_Matrix(4)
    # calculate half_height, half_width, and pixel size
    half_view = math.tan(self.field_of_view / 2.0)
    aspect = self.hsize / self.vsize
    if aspect >= 1:
      self.half_width = half_view
      self.half_height = half_view / aspect
    else:
      self.half_width = half_view * aspect
      self.half_height = half_view
    self.pixel_size = (self.half_width * 2.0) / self.hsize

  def ray_for_pixel(self, px, py):
    xoffset = (px + 0.5) * self.pixel_size
    yoffset = (py + 0.5) * self.pixel_size
    worldx = self.half_width - xoffset
    worldy = self.half_height - yoffset
    inv_transform = self.transform.inverse()
    pixel = inv_transform * Point(worldx, worldy, -1.0)
    origin = inv_transform * Point(0, 0, 0)
    direction = pixel.subtract(origin).normalize()
    return Ray(origin, direction)

  def render(self, world):
    image = Canvas(self.hsize, self.vsize)
    for y in range(self.vsize):
      for x in range(self.hsize):
        ray = self.ray_for_pixel(x, y)
        color = world.color_at(ray)
        image.write_pixel(x, y, color)
    return image
