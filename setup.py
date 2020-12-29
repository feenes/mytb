# python std modules

# third party modules
from setuptools import find_packages
from setuptools import setup

long_description = """small modules and tools useful for many projects
"""

setup(name="mytb",
      version="0.1.0",
      description="my toolbox for everyday python projects",
      long_description=long_description,
      long_description_content_type="text/x-rst",
      classifiers=[
            "Development Status :: 3 - Alpha",
      ],
      keywords="toolbox development",
      url="https://github.com/feenes",
      author="Teledomic",
      author_email="info@teledomic.eu",
      license="MIT",
      packages=find_packages(),
      scripts=[],
      entry_points={
          "console_scripts": [
            "mytb = mytb.commands:main",
            ]
      },
      project_urls={
        "Homepage": "https://github.com/feenes/mytb",
        "Documentation": "https://github.com/feenes/mytb",
        "Source": "https://github.com/feenes/mytb",
        "SayThanks": "https://github.com/feenes",
        "Funding": "https://donate.pypi.org",
        "Tracker": "https://github.com/feenes/mytb/issues",
      },
      install_requires=[
        "minibelt",
        ],
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
      python_requires=">=3.5, <4",
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],
      zip_safe=False,
      include_package_data=True,
      )
