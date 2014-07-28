from setuptools import setup, find_packages
import os

version = '1.1'

setup(name='abstract.richdescription',
      version=version,
      description="Abstract Rich Description",
      long_description=open("README.md").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Biagio Grimaldi',
      author_email='biagio.grimaldi@abstract.it',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['abstract'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.CMFCore',
          'archetypes.schemaextender',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=[],
      paster_plugins=["ZopeSkel"],
      )
