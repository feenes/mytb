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
      version='0.0.4',
      description='my toolbox for everyday python projects',
      long_description="small modules and tools useful for many projects",
      long_description_content_type="text/x-rst",
      classifiers=[
            'Development Status :: 3 - Alpha',
            #'Intendened Audience ::  Developers',
            #'Topic :: Software Development :: Modules',
            #'License :: OSI Approved :: MIT License',
            
            #'Programming Language :: Python :: 2',
            #'Programming Language :: Python :: 2.7',

            #'Programming Language :: Python :: 3',
            #'Programming Language :: Python :: 3.5',
            #'Programming Language :: Python :: 3.6',
      ],
      keywords='toolbox development',
      url='https://www.teledomic.eu',
      author='Teledomic',
      author_email='info@teledomic.eu',
      license="MIT",
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
      project_urls={
        'Documentation': "https://github.com/feenes/mytb",
        'Source': "https://github.com/feenes/mytb",
        'SayThanks': "https://github.com/feenes",
        'Funding': 'https://donate.pypi.org',
        'Tracker': "https://github.com/feenes/mytb/issues",
      },
      test_suite='nose.collector',
      install_requires=install_requires,
      tests_require=['nose', 'ddt'],
      zip_safe = False,
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
      )
