import codecs
import os
import sys
 
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

NAME = "django-simple-serializer"
 
PACKAGES = ["dss", ]
 
DESCRIPTION = "Django Simple Serializer is a serializer to help user serialize django data or python list into json,xml,dict data in a simple way."
 
LONG_DESCRIPTION = read("README.rst")
 
KEYWORDS = "django serializer"

AUTHOR = "RaPoSpectre"
 
AUTHOR_EMAIL = "rapospectre@gmail.com"
 
URL = "https://github.com/bluedazzle/django-simple-serializer"
 
VERSION = "2.0.3"

LICENSE = "MIT"

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)