from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='my315ok.wechat',
      version=version,
      description="a chat platform for TengXun Weixin",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='python plone',
      author='Adam tang',
      author_email='yuejun.tang@gmail.com',
      url='https://github.com/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['my315ok'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'WeRoBot=1.10.0',
          'plone.app.registry',           
          'plone.app.dexterity',
          'plone.directives.form',
          'plone.app.z3cform',
          'my315ok.products',
          'five.globalrequest',
          'five.grok',
          'requests',
          'six',
#           'PIL',          
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': ['plone.app.testing',]
      },         
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
#      setup_requires=["PasteScript"],
#      paster_plugins=["ZopeSkel"],
      )
