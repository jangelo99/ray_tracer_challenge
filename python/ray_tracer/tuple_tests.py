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
  
  def test_equals(self):
    self.assertTrue(self.pt_a.equals(Point(4.3, -4.2, 3.1)))
    self.assertTrue(self.vec_a.equals(Vector(4.3, -4.2, 3.1)))
    self.assertFalse(self.pt_a.equals(self.vec_a))

if __name__ == '__main__':
    unittest.main()
