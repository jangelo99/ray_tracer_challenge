
from operator import itemgetter

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


class Ray:
  def __init__(self, origin, direction):
    self.origin = origin
    self.direction = direction
    self.intersections = []

  def position(self, t):
    return self.origin.add(self.direction.scalar_multiply(t))

  def intersect(self, shape):
    ray2 = self.transform(shape.transform.inverse())
    xs = shape.intersect(ray2)
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
