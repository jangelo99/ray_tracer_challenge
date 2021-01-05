import unittest

from tuple import Point, Vector

class TupleTestCase(unittest.TestCase):

  def setUp(self):
    self.pt_a = Point(4.3, -4.2, 3.1)
    self.vec_a = Vector(4.3, -4.2, 3.1)
    
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

if __name__ == '__main__':
    unittest.main()
