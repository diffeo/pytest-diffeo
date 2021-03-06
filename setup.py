#!/usr/bin/env python

from __future__ import absolute_import
import os
from setuptools import setup, find_packages
import version

def read_file(fn):
    with open(os.path.join(os.path.dirname(__file__), fn), 'r') as f:
        return f.read()

VERSION, SOURCE_LABEL = version.get_git_version()
setup(name='pytest-diffeo',
      version=VERSION,
      description='Common py.test support for Diffeo packages',
      url='https://github.com/diffeo/pytest-diffeo',
      license='MIT/X11 license http://opensource.org/licenses/MIT',
      long_description=read_file('README.rst'),
      author='Diffeo, Inc.',
      author_email='support@diffeo.com',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'pytest',
          # 'pytest-capturelog',
          'six',
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Topic :: Utilities',
          'License :: OSI Approved :: MIT License',  ## MIT/X11 license http://opensource.org/licenses/MIT
      ],
      entry_points={
          'pytest11': [
              'diffeo = pytest_diffeo',
          ]
      }
)
