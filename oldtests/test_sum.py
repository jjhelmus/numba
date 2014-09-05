#! /usr/bin/env python
# ______________________________________________________________________
'''test_sum

Test the sum2d() example.
'''
# ______________________________________________________________________

import numpy

from numba import *
import unittest

# ______________________________________________________________________

def sum2d(arr):
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

# ______________________________________________________________________

def bad_sum2d(arr):
    '''Unit test code for issue #34:
    https://github.com/numba/numba/issues/34'''
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
        return result

# ______________________________________________________________________

class TestASTSum2d(unittest.TestCase):

    def test_vectorized_sum2d(self):
        usum2d = jit(argtypes=[double[:,:]],
                          restype=double)(sum2d)
        image = numpy.random.rand(10, 10)
        plain_old_result = sum2d(image)
        hot_new_result = usum2d(image)
        self.assertTrue((abs(plain_old_result - hot_new_result) < 1e-9).all())

    def test_vectorized_sum2d(self):
        usum2d = jit(argtypes=[double[:,:]],
                          restype=double)(sum2d)
        image = numpy.random.rand(10, 10)
        plain_old_result = sum2d(image)
        hot_new_result = usum2d(image)
        self.assertTrue((abs(plain_old_result - hot_new_result) < 1e-9).all())

    def _bad_sum2d(self):
        compiled_bad_sum2d = self.jit(argtypes = [double[:,:]],
                                      restype = double)(bad_sum2d)
        image = numpy.random.rand(10, 10)
        self.assertEqual(bad_sum2d(image), compiled_bad_sum2d(image))

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_sum.py