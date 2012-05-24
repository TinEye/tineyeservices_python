from setuptools import setup, find_packages
import sys, os

version = '1.0.1'

setup(name='tineyeservices',
      version=version,
      description="Python client for the MatchEngine, MobileEngine, and MulticolorEngine APIs.",
      long_description="""\
MatchEngine, MobileEngine and MulticolorEngine are general image matching engines that allow you to perform large scale image comparisons for a variety of tasks.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='image search',
      author='Id\xc3\xa9e Inc.',
      author_email='support@tineye.com',
      url='http://tineye.com/',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'requests'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
