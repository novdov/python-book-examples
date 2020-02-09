from setuptools import setup

from Cython.Build import cythonize

setup(name="nbdoy", ext_modules=cythonize("nbody.pyx"))
