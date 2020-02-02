cdef extern from "cfib.h":
    unsigned long _fib "fib"(unsigned long n)


def fib(n):
    return _fib(n)
