import unittest

from matrix import Matrix

class MatrixTestCase(unittest.TestCase):

  def test_matrix_create(self):
    # 4x4 matrix
    A = Matrix([[1, 2, 3, 4], [5.5, 6.5, 7.5, 8.5], [9, 10, 11, 12], [13.5, 14.5, 15.5, 16.5]])
    self.assertEqual(A[0, 0], 1.0)
    self.assertEqual(A[0, 3], 4.0)
    self.assertEqual(A[1, 0], 5.5)
    self.assertEqual(A[1, 2], 7.5)
    self.assertEqual(A[2, 2], 11.0)
    self.assertEqual(A[3, 0], 13.5)
    self.assertEqual(A[3, 2], 15.5)
    # 3x3 matrix
    B = Matrix([[-3, 5, 0], [1, -2, -7], [0, 1, 1]])
    self.assertEqual(B[0, 0], -3.0)
    self.assertEqual(B[1, 1], -2.0)
    self.assertEqual(B[2, 2], 1.0)

  def test_matrix_equality(self):
    A = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    B = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    self.assertTrue(A == B)
    C = Matrix([[1, 2, 3, 4], [5.5, 6.5, 7.5, 8.5], [9, 10, 11, 12], [13.5, 14.5, 15.5, 16.5]])
    self.assertTrue(A != C)
