# -*- coding: utf-8 -*-
# Copyright (c) 2017 TinEye. All rights reserved worldwide.

from setuptools import setup, find_packages

version = '1.6.2'

setup(name='tineyeservices',
      version=version,
      description="Python client for the MatchEngine, MobileEngine, MulticolorEngine and WineEngine APIs.",
      long_description="""\
MatchEngine, MobileEngine, MulticolorEngine and WineEngine are general image matching engines that allow you to perform large scale image comparisons for a variety of tasks.""",
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='reverse image search',
      author='TinEye',
      author_email='support@tineye.com',
      url='https://services.tineye.com/',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'requests>=2.7.0,<3.0'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
