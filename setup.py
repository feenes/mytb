from __future__ import absolute_import
from __future__ import print_function

import os, sys

from setuptools import setup

install_requires = [
    'minibelt',
]

setup(name='mytb',
      version='0.0.2',
      description='my toolbox for everyday python projects',
      classifiers=[
      ],
      keywords='toolbox',
      url='https://www.teledomic.eu',
      author='Teledomic',
      author_email='info@teledomic.eu',
      packages=[
            'mytb', 
            'mytb.importlib', 
            'mytb.logging', 
            'mytb.logging.handlers', 
            'mytb.tests', 
            ],
      scripts=[],
      entry_points={
          'console_scripts': [ ]
      },
      test_suite='nose.collector',
      install_requires=install_requires,
      tests_require=['nose'],
      zip_safe = False)

