from __future__ import print_function

import numpy

import numba.unittest_support as unittest
from numba.ctypes_support import *
from numba import _helperlib


class ArrayStruct3D(Structure):
    # Mimick the structure defined in numba.targets.arrayobj's make_array()
    _fields_ = [
        ("parent", c_void_p),
        ("data", c_void_p),
        ("shape", (c_ssize_t * 3)),
        ("strides", (c_ssize_t * 3)),
    ]


class TestArrayAdaptor(unittest.TestCase):
    def test_array_adaptor(self):
        arystruct = ArrayStruct3D()

        adaptorptr = _helperlib.c_helpers['adapt_ndarray']
        adaptor = PYFUNCTYPE(c_int, py_object, c_void_p)(adaptorptr)

        ary = numpy.arange(60).reshape(2, 3, 10)
        status = adaptor(ary, byref(arystruct))
        self.assertEqual(status, 0)
        self.assertEqual(arystruct.data, ary.ctypes.data)
        self.assertEqual(arystruct.parent, id(ary))
        for i in range(3):
            self.assertEqual(arystruct.shape[i], ary.ctypes.shape[i])
            self.assertEqual(arystruct.strides[i], ary.ctypes.strides[i])


if __name__ == '__main__':
    unittest.main()
