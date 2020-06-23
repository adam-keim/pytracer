from raytracer.base import Matrix, Tuple, Identity


def test_4x4_matrix():
    m = Matrix(
        [[1, 2, 3, 4], [5.5, 6.5, 7.5, 8.5], [9, 10, 11, 12], [13.5, 14.5, 15.5, 16.5],]
    )
    assert m[0][0] == 1
    assert m[0][3] == 4
    assert m[1][0] == 5.5
    assert m[1][2] == 7.5
    assert m[2][2] == 11
    assert m[3][0] == 13.5
    assert m[3][2] == 15.5


def test_2x2_matrix():
    m = Matrix([[-3, 5], [1, -2]])
    assert m[0][0] == -3
    assert m[0][1] == 5
    assert m[1][0] == 1
    assert m[1][1] == -2


def test_3x3_matrix():
    m = Matrix([[-3, 5, 0], [1, -2, -7], [0, 1, 1]])
    assert m[0][0] == -3
    assert m[1][1] == -2
    assert m[2][2] == 1


def test_matrix_equality():
    m1 = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [2, 3, 4, 5], [3, 4, 5, 6]])
    m2 = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [2, 3, 4, 5], [3, 4, 5, 6]])
    assert m1 == m2


def test_matrix_inequality():
    m1 = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [2, 3, 2, 5], [3, 4, 5, 6]])
    m2 = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [2, 3, 4, 5], [3, 4, 5, 6]])
    assert m1 != m2


def test_matrix_mult():
    m1 = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 8, 7, 6], [5, 4, 3, 2]])
    m2 = Matrix([[-2, 1, 2, 3], [3, 2, 1, -1], [4, 3, 6, 5], [1, 2, 7, 8]])
    m3 = Matrix(
        [[20, 22, 50, 48], [44, 54, 114, 108], [40, 58, 110, 102], [16, 26, 46, 42]]
    )
    assert m1 * m2 == m3


def test_tuple_mult():
    m = Matrix([[1, 2, 3, 4], [2, 4, 4, 2], [8, 6, 4, 1], [0, 0, 0, 1]])
    t = Tuple(1, 2, 3, 1)
    assert m * t == Tuple(18, 24, 33, 1)


def test_identity_mult():
    m = Matrix([[0, 1, 2, 4], [1, 2, 4, 8], [2, 4, 8, 16], [4, 8, 16, 32]])
    i = Identity()
    assert m * i == m


def test_transpose():
    m1 = Matrix([[0, 9, 3, 0], [9, 8, 0, 8], [1, 8, 5, 3], [0, 0, 5, 8]])
    m2 = Matrix([[0, 9, 1, 0], [9, 8, 8, 0], [3, 0, 5, 5], [0, 8, 3, 8]])
    assert m1.transpose() == m2


def test_identity_transpose():
    m = Identity()
    assert m == m.transpose()


def test_2x2_determinant():
    m = Matrix([[1, 5], [-3, 2]])
    assert m.determinant() == 17


def test_2x2_sub():
    m = Matrix([[1, 5, 0], [-3, 2, 7], [0, 6, -3]])
    sub = m.sub(0, 2)
    assert sub == Matrix([[-3, 2], [0, 6]])


def test_3x3_sub():
    m = Matrix([[-6, 1, 1, 6], [-8, 5, 8, 6], [-1, 0, 8, 2], [-7, 1, -1, 1]])
    sub = m.sub(2, 1)
    assert sub == Matrix([[-6, 1, 6], [-8, 8, 6], [-7, -1, 1]])


def test_minor():
    m = Matrix([[3, 5, 0], [2, -1, -7], [6, -1, 5]])
    b = m.sub(1, 0)
    assert b.determinant() == 25
    assert m.minor(1, 0) == 25


def test_cofactor():
    m = Matrix([[3, 5, 0], [2, -1, -7], [6, -1, 5]])
    assert m.minor(0, 0) == -12
    assert m.cofactor(0, 0) == -12
    assert m.minor(1, 0) == 25
    assert m.cofactor(1, 0) == -25


def test_3x3_determinant():
    m = Matrix([[1, 2, 6], [-5, 8, -4], [2, 6, 4]])
    assert m.cofactor(0, 0) == 56
    assert m.cofactor(0, 1) == 12
    assert m.cofactor(0, 2) == -46
    assert m.determinant() == -196


def test_4x4_determinant():
    m = Matrix([[-2, -8, 3, 5], [-3, 1, 7, 3], [1, 2, -9, 6], [-6, 7, 7, -9]])
    assert m.cofactor(0, 0) == 690
    assert m.cofactor(0, 1) == 447
    assert m.cofactor(0, 2) == 210
    assert m.cofactor(0, 3) == 51
    assert m.determinant() == -4071


def test_invertibility():
    m1 = Matrix([[6, 4, 4, 4], [5, 5, 7, 6], [4, -9, 3, -7], [9, 1, 7, -6]])
    assert m1.determinant() == -2120
    assert m1.invertible()

    m2 = Matrix([[-4, 2, -2, -3], [9, 6, 2, 6], [0, -5, 1, -5], [0, 0, 0, 0]])
    assert m2.determinant() == 0
    assert m2.invertible() == False


def test_inverse():
    a = Matrix([[-5, 2, 6, -8], [1, -5, 1, 8], [7, 7, -6, -7], [1, -3, 7, 4]])
    b = a.inverse()
    assert a.determinant() == 532
    assert a.cofactor(2, 3) == -160
    assert b[3][2] == -160 / 532
    assert a.cofactor(3, 2) == 105
    assert b[2][3] == 105 / 532
    b_exp = Matrix(
        [
            [0.21805, 0.45113, 0.24060, -0.04511],
            [-0.80827, -1.45677, -0.44361, 0.52068],
            [-0.07895, -0.22368, -0.05263, 0.19737],
            [-0.52256, -0.81391, -0.30075, 0.30639],
        ]
    )
    assert b_exp == b


def test_more_inverse():
    a = Matrix([[8, -5, 9, 2], [7, 5, 6, 1], [-6, 0, 9, 6], [-3, 0, -9, -4]])
    a_exp = Matrix(
        [
            [-0.15385, -0.15385, -0.28205, -0.53846],
            [-0.07692, 0.12308, 0.02564, 0.03077],
            [0.35897, 0.35897, 0.43590, 0.92308],
            [-0.69231, -0.69231, -0.76923, -1.92308],
        ]
    )
    assert a.inverse() == a_exp

    b = Matrix([[9, 3, 0, 9], [-5, -2, -6, -3], [-4, 9, 6, 4], [-7, 6, 6, 2]])
    b_exp = Matrix(
        [
            [-0.04074, -0.07778, 0.14444, -0.22222],
            [-0.07778, 0.03333, 0.36667, -0.33333],
            [-0.02901, -0.14630, -0.10926, 0.12963],
            [0.17778, 0.06667, -0.26667, 0.33333],
        ]
    )
    assert b.inverse() == b_exp


def test_inverse_mult():
    a = Matrix([[3, -9, 7, 3], [3, -8, 2, -9], [-4, 4, 4, 1], [-6, 5, -1, 1]])
    b = Matrix([[8, 2, 2, 2], [3, -1, 7, 0], [7, 0, 5, 4], [6, -2, 0, 5]])
    c = a * b
    assert c * b.inverse() == a
