import unittest

from matrix import Matrix
from tuple import Point, Vector

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

  def test_matrix_multiply(self):
    # multiply matrix by matrix
    A = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
    B = Matrix([[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]])
    result = A * B
    self.assertEqual(result, Matrix([[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102], [16, 26, 46, 42]]))
    # multiply matrix by tuples
    C = Matrix([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
    d = Point(1, 2, 3)
    result = C * d
    self.assertTrue(result.equals(Point(18, 24, 33)))
    d = Vector(1, 2, 3)
    result = C * d
    self.assertTrue(result.equals(Vector(14, 22, 32)))
