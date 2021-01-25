

class Ray:
  def __init__(self, origin, direction):
    self.origin = origin
    self.direction = direction

  def position(self, t):
    return self.origin.add(self.direction.scalar_multiply(t))
