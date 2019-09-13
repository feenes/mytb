from __future__ import absolute_import, print_function
# python std modules

# third party modules
from setuptools import setup

install_requires = [
    "future",
    "minibelt",
]

setup(name="mytb",
      version="0.0.11",
      author="Teledomic",
      author_email="info@teledomic.eu",
      description="my toolbox for everyday python projects",
      long_description="small modules and tools useful for many projects",
      long_description_content_type="text/x-rst",
      classifiers=[
            "Development Status :: 3 - Alpha",
      ],
      keywords="toolbox development",
      license="MIT",
      packages=[
            "mytb",
            "mytb.commands",
            "mytb.importlib",
            "mytb.gitlab",
            "mytb.html",
            "mytb.logging",
            "mytb.logging.configs",
            "mytb.logging.handlers",

            # might comment if you want that the dist package implements
            # no tests
            "mytb.tests",
            "mytb.tests.gitlab",
            ],
      scripts=[],
      entry_points={
          "console_scripts": [
            "mytb = mytb.commands:main",
            ]
      },
      project_urls={
        "Homepage": "https://github.com/feenes",
        "Documentation": "https://github.com/feenes/mytb",
        "Source": "https://github.com/feenes/mytb",
        "SayThanks": "https://github.com/feenes",
        "Funding": "https://donate.pypi.org",
        "Tracker": "https://github.com/feenes/mytb/issues",
      },
      install_requires=install_requires,
      extras_require=dict(
        minimal=[],
        all=[
            "dateutils",
            "pytz",
            "tzlocal",
            "pyyaml",
            ],
        date=[
            "dateutils",
            "pytz",
            "tzlocal",
            ],
        gitlab=[
            "pyyaml",
            ],
        ),
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],
      zip_safe=False,
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
      )
