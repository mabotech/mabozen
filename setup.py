import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
    'flask',  
    'mako',
    'simplejson'
    ]

setup(name='mabozen',
    version='0.0.2',
    description='mabozen webapp generator',
    long_description=README + '\n\n' +  CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: webapp",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='MaboTech',
    license='MIT',
    author_email='mes@mabotech.com',
    url='http://www.mabotech.com',
    keywords='mabotech webapp general generator',

    zip_safe=False,
    test_suite='mabozen',
    install_requires = requires,

    include_package_data=True,
    packages=find_packages(),
    package_dir={'mabozen': 'mabozen'},
    package_data={'mabozen': ['conf/*.*']}
  )

