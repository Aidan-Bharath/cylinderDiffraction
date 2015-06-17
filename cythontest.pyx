from __future__ import division
from libc.math cimport sqrt,atan
import numpy as np
cimport numpy as np


DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

cpdef test(np.ndarray[DTYPE_t, ndim=1] x, np.ndarray[DTYPE_t, ndim=1] y):

    cdef: 
        int i
        int xs = x.shape[0]
        np.ndarray[DTYPE_t,ndim=1] b = np.zeros([xs])

    for i in xrange(xs):
        b[i] = x[i]*y[i]

    return b


cdef double cartToPol(double x,double y):
    ## Watch this returns negative values below x axis
    return sqrt(x**2+y**2),atan(y/x)

def looptest(np.ndarray[DTYPE_t,ndim = 1] x,np.ndarray[DTYPE_t,ndim = 1] y):
    int 
