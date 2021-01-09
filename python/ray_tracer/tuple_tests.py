import math
import unittest

from tuple import Point, Vector, InvalidOperationError

class TupleTestCase(unittest.TestCase):

  def setUp(self):
    self.pt_a = Point(4.3, -4.2, 3.1)
    self.pt_b = Point(3.0, -2.0, 5.0)
    self.vec_a = Vector(4.3, -4.2, 3.1)
    self.vec_b = Vector(3.0, -2.0, 5.0)
    
  def test_pt_a(self):
    self.assertEqual(self.pt_a.x, 4.3)
    self.assertEqual(self.pt_a.y, -4.2)
    self.assertEqual(self.pt_a.z, 3.1)
    self.assertEqual(self.pt_a.w, 1.0)
    self.assertTrue(self.pt_a.is_point())
    self.assertFalse(self.pt_a.is_vector())

  def test_vec_a(self):
    self.assertEqual(self.vec_a.x, 4.3)
    self.assertEqual(self.vec_a.y, -4.2)
    self.assertEqual(self.vec_a.z, 3.1)
    self.assertEqual(self.vec_a.w, 0.0)
    self.assertFalse(self.vec_a.is_point())
    self.assertTrue(self.vec_a.is_vector())

  def test_equals(self):
    self.assertTrue(self.pt_a.equals(Point(4.3, -4.2, 3.1)))
    self.assertTrue(self.vec_a.equals(Vector(4.3, -4.2, 3.1)))
    self.assertFalse(self.pt_a.equals(self.vec_a))
    
  def test_add(self):
    # adding 2 vectors produces a vector
    add_vecs = self.vec_a.add(self.vec_b)
    self.assertEqual(add_vecs.x, 7.3)
    self.assertEqual(add_vecs.y, -6.2)
    self.assertEqual(add_vecs.z, 8.1)
    self.assertEqual(add_vecs.w, 0.0)
    # adding a vector to a point produces a point
    add_vec_to_pt = self.pt_a.add(self.vec_a)
    self.assertEqual(add_vec_to_pt.x, 8.6)
    self.assertEqual(add_vec_to_pt.y, -8.4)
    self.assertEqual(add_vec_to_pt.z, 6.2)
    self.assertEqual(add_vec_to_pt.w, 1.0)
    # adding a point to a vector produces a point
    add_pt_to_vec = self.vec_b.add(self.pt_a)
    self.assertEqual(add_pt_to_vec.x, 7.3)
    self.assertEqual(add_pt_to_vec.y, -6.2)
    self.assertEqual(add_pt_to_vec.z, 8.1)
    self.assertEqual(add_pt_to_vec.w, 1.0)
    # adding 2 points raises an exception
    with self.assertRaises(InvalidOperationError):
      add_pts = self.pt_a.add(self.pt_b)
  
  def test_subtract(self):
    # subtracting a vector from a vector produces a vector
    v1 = Vector(3, 2, 1)
    v2 = Vector(5, 6, 7)
    result = v1.subtract(v2)
    self.assertTrue(result.equals(Vector(-2, -4, -6)))
    # subtracting a point from a point produces a vector
    p1 = Point(3, 2, 1)
    p2 = Point(5, 6, 7)
    result = p1.subtract(p2)
    self.assertTrue(result.equals(Vector(-2, -4, -6)))
    # subtracting a vector from a point produces a point
    result = p1.subtract(v2)
    self.assertTrue(result.equals(Point(-2, -4, -6)))
    # subtracting a point from a vector raises an exception
    with self.assertRaises(InvalidOperationError):
      result = v1.subtract(p2)

  def test_scalar_multiply(self):
    v1 = Vector(1, -2, 3)
    result = v1.scalar_multiply(3.5)
    self.assertTrue(result.equals(Vector(3.5, -7.0, 10.5)))
    v2 = Vector(1, -2, 3)
    result = v2.scalar_multiply(0.5)
    self.assertTrue(result.equals(Vector(0.5, -1.0, 1.5)))

  def test_scalar_divide(self):
    v1 = Vector(1, -2, 3)
    result = v1.scalar_divide(2.0)
    self.assertTrue(result.equals(Vector(0.5, -1.0, 1.5)))

  def test_negate(self):
    v1 = Vector(1, -2, 3)
    result = v1.negate()
    self.assertTrue(result.equals(Vector(-1, 2, -3)))

  def test_magnitude(self):
    v1 = Vector(0, 1, 0)
    v2 = Vector(1, 2, 3)
    v3 = Vector(-1, -2, -3)
    self.assertEqual(v1.magnitude(), 1.0)
    self.assertEqual(v2.magnitude(), math.sqrt(14))
    self.assertEqual(v3.magnitude(), math.sqrt(14))

  def test_normalize(self):
    v1 = Vector(0, 4, 0)
    result = v1.normalize()
    self.assertEqual(result.magnitude(), 1.0)
    self.assertTrue(result.equals(Vector(0, 1, 0)))
    v2 = Vector(1, 2, 3)
    result = v2.normalize()
    self.assertEqual(result.magnitude(), 1.0)
    self.assertTrue(result.equals(Vector(1.0/math.sqrt(14), 2.0/math.sqrt(14), 3.0/math.sqrt(14))))
    v3 = Vector(0, 0, 0)
    with self.assertRaises(InvalidOperationError):
      result = v3.normalize()

  def test_dot_product(self):
    v1 = Vector(1, 2, 3)
    v2 = Vector(2, 3, 4)
    self.assertEqual(v1.dot(v2), 20.0)

  def test_cross_product(self):
    v1 = Vector(1, 2, 3)
    v2 = Vector(2, 3, 4)
    result = v1.cross(v2)
    self.assertTrue(result.equals(Vector(-1, 2, -1)))
    result = v2.cross(v1)
    self.assertTrue(result.equals(Vector(1, -2, 1)))

if __name__ == '__main__':
    unittest.main()
