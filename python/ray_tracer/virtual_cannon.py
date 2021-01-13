
from canvas import Canvas, Color
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
  
  canvas = Canvas(900, 550)
  red = Color(1, 0, 0)
  canvas.write_pixel(start.x, canvas.height - start.y, red)

  while p.position.y > 0:
    p = tick(e, p)
    x = round(p.position.x)
    y = canvas.height - round(p.position.y)
    canvas.write_pixel(x, y, red)
    print("x=" + str(x) + ", y=" + str(y))

  print("Writing canvas to PPM file...")
  canvas.to_ppm("canvas.ppm")
