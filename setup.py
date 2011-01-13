from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='ql.backend',
      version=version,
      description="a RESTful backend for storing content",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='quantumloung restful api content cms mongo',
      author='Christian Scholz',
      author_email='cs@comlounge.net',
      url='http://quantumlounge.org/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ql'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pymongo',
          'logbook',
          'Routes',
          'werkzeug',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
