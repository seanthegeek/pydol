#!/usr/bn/env python
# -*- coding: utf-8 -*-

"""Setup script for pydol"""

# pylint: disable=F0401
# pylint: disable=E0611

from distutils.core import setup

__author__ = "Sean Whalen"
__copyright__ = "Copyright 2016 %s" % __author__
__license__ = "Apache 2.0"
license_text = """Copyright 2016 Sean Whalen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""


def get_requirements():
    with open("requirements.txt") as requirements_file:
        return map(lambda line: line.trim(), requirements_file.read().split('\n'))

def get_readme():
    with open("README.rst") as readme_file:
        return readme_file.read()

setup(name="pydol",
      version="1.0.3",
      description="A pythonic interface to the U.S. Department of Labor API",
      license=license_text,
      author="Sean Whalen",
      url='https://github.com/seanthegeek/pydol',
      author_email="whalenster@gmail.com",
      packages=['pydol', 'pydol.test'],
      long_description=get_readme(),
      install_requires=get_requirements(),
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Legal Industry',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Education',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Utilities'])
