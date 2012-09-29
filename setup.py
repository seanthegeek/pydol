#!/usr/bn/env python
# -*- coding: utf-8 -*-

"""Setup script for pydol"""

# pylint: disable=F0401
# pylint: disable=E0611

from distutils.core import setup

__author__ = "Sean Whalen"
__copyright__ = "Copyright (C) 2012 %s" % __author__
__license__ = "MIT"


setup(name="pydol",
      version="1.0.1",
      description="A pythonic interface to the U.S. Department of Labor API",
      license=open('LICENSE.txt').read(),
      author="Sean Whalen",
      url='https://github.com/seanthegeek/pydol',
      author_email="whalenster@gmail.com",
      packages=['pydol', 'pydol.test'],
      long_description=open('README.rst').read(),
      install_requires=["requests", "xmltodict"],
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Legal Industry',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Education',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Utilities'])
