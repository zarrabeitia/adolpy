#!/usr/bin/env python
#
# Distutils setup script for adolpy 
#
# $Id$
# ---------------------------------------------------------------------------

from distutils.core import setup
import re
import os
import sys
import imp

# Load the data.

here = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path = [here] + sys.path
mf = os.path.join(here, 'adolpy')
adolpy = imp.load_package('adolpy', mf) 
long_description = adolpy.__doc__
version = str(adolpy.__version__)
author = adolpy.__author__
email = adolpy.__email__

url = adolpy.__url__
license = adolpy.__license__

setup(
    name="adolpy",
    version=version,
    description="Automatic differentiation using the forward model",
    long_description=long_description,
    url=url,
    license=license,
    author=author,
    author_email=email,
    package_dir = {"adolpy": mf},
    packages=["adolpy"],
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GPLv3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
