
class Intersection:
  def __init__(self, t, shape):
    self.t = t
    self.shape = shape


class Ray:
  def __init__(self, origin, direction):
    self.origin = origin
    self.direction = direction

  def position(self, t):
    return self.origin.add(self.direction.scalar_multiply(t))


def intersect(shape, ray):
  xs = shape.intersect(ray)
  if len(xs) > 0:
    intersections = list()
    for t in xs:
      intersections.append(Intersection(t, shape))
    return intersections
  else:
    return []
