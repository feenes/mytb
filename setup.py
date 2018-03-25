from __future__ import absolute_import, print_function

# python std modules
import os
import sys

# third party modules
from setuptools import setup

install_requires = [
    'begins',
    'minibelt',
    'pyyaml',
]

setup(name='mytb',
      version='0.0.3',
      description='my toolbox for everyday python projects',
      classifiers=[
      ],
      keywords='toolbox',
      url='https://www.teledomic.eu',
      author='Teledomic',
      author_email='info@teledomic.eu',
      packages=[
            'mytb', 
            'mytb.commands', 
            'mytb.importlib', 
            'mytb.logging', 
            'mytb.gitlab', 
            'mytb.logging.handlers', 

            # might uncomment if you want that the dist package implements no tests
            'mytb.tests', 
            'mytb.tests.gitlab', 
            ],
      scripts=[],
      entry_points={
          'console_scripts': [ 
            'mytb = mytb.commands:main',
            ]
      },
      test_suite='nose.collector',
      install_requires=install_requires,
      tests_require=['nose', 'ddt'],
      zip_safe = False)
