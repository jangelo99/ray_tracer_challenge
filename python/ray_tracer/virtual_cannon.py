
from tuple import Point, Vector

class Projectile():
  def __init__(self, position, velocity):
    self.position = position
    self.velocity = velocity

class Environment():
  def __init__(self, gravity, wind):
    self.gravity = gravity
    self.wind = wind
    
def tick(env, proj):
  position = proj.position.add(proj.velocity)
  velocity = proj.velocity.add(env.gravity.add(env.wind))
  return Projectile(position, velocity)

if __name__ == '__main__':

  start = Point(0, 1, 0)
  velocity = Vector(1, 1.8, 0).normalize().scalar_multiply(11.25)
  p = Projectile(start, velocity)

  gravity = Vector(0, -0.1, 0)
  wind = Vector(-0.01, 0, 0)
  e = Environment(gravity, wind)
  
  while p.position.y > 0:
    p = tick(e, p)
    print("x=" + str(p.position.x) + ", y=" + str(p.position.y))