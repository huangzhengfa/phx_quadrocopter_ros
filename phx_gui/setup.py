#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['phx_gui'],
    package_dir={'': 'src'},
    scripts=['scripts/phx_gui']
)

setup(**d)
