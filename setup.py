#!/usr/bin/env python

import os.path
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, "README.rst")).read()
    CHANGES = open(os.path.join(here, "CHANGES")).read()
except IOError:
    README = CHANGES = ""


setup(
    name="muttd",
    version="0.2.0",
    description="Mail viewer for mutt",
    long_description=README + "\n\n" + CHANGES,
    author="Bertrand Janin",
    author_email="b@janin.com",
    url="http://github.com/debsquad/muttd/",
    scripts=["bin/muttd"],
    license="ISC License (ISCL, BSD/MIT compatible)",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD",
        "Programming Language :: Python :: 3.3",
        "Topic :: Communications :: Email",
    ],
    install_requires=[
        "six",
    ],
    test_requires=[
        "nose",
        "coverage",
    ],
)
