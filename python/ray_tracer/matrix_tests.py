import unittest

from matrix import Matrix, Identity_Matrix, Translation_Matrix, Scaling_Matrix
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

  def test_identity_matrix(self):
    I = Identity_Matrix(4)
    self.assertEqual(I, Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))
    A = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
    result = A * I
    self.assertEqual(result, A)
    b = Point(1, 2, 3)
    result = I * b
    self.assertTrue(result.equals(Point(1, 2, 3)))
    c = Vector(4, 5, 6)
    result = I * c
    self.assertTrue(result.equals(Vector(4, 5, 6)))

  def test_matrix_transpose(self):
    A = Matrix([[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]])
    A_transpose = Matrix([[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]])
    result = A.transpose()
    self.assertEqual(result, A_transpose)
    I = Identity_Matrix(4)
    result = I.transpose()
    self.assertEqual(result, Identity_Matrix(4))

  def test_matrix_determinant(self):
    A = Matrix([[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])
    result = A.determinant()
    self.assertEqual(result, -4071.0)

  def test_matrix_inverse(self):
    A = Matrix([[-5, 2, 6, -8], [1, -5, 1, 8], [7, 7, -6, -7], [1, -3, 7, 4]])
    A_inv = Matrix([[0.21805, 0.45113, 0.24060, -0.04511], [-0.80827, -1.45677, -0.44361, 0.52068], \
                    [-0.07895, -0.22368, -0.05263, 0.19737], [-0.52256, -0.81391, -0.30075, 0.30639]])
    result = A.inverse()
    self.assertTrue(result == A_inv)
    result = A * A.inverse()
    self.assertEqual(result, Identity_Matrix(4))

  def test_translation_matrix(self):
    T = Translation_Matrix(5, -3, 2)
    p = Point(-3, 4, 5)
    result = T * p
    self.assertTrue(result.equals(Point(2, 1, 7)))
    T_inv = T.inverse()
    result = T_inv * p
    self.assertTrue(result.equals(Point(-8, 7, 3)))
    v = Vector(-3, 4, 5)
    result = T * v
    self.assertTrue(result.equals(v))

  def test_scaling_matrix(self):
    T = Scaling_Matrix(2, 3, 4)
    p = Point(-4, 6, 8)
    result = T * p
    self.assertTrue(result.equals(Point(-8, 18, 32)))
    T_inv = T.inverse()
    result = T_inv * p
    self.assertTrue(result.equals(Point(-2, 2, 2)))
    v = Vector(-4, 6, 8)
    result = T * v
    self.assertTrue(result.equals(Vector(-8, 18, 32)))
    # use scaling matrix for reflection around x-axis
    T = Scaling_Matrix(-1, 1, 1)
    result = T * p
    self.assertTrue(result.equals(Point(4, 6, 8)))
