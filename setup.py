#!/usr/bin/env python

from setuptools import find_packages, setup


def read(filename):
    with open(filename) as fp:
        return fp.read()


setup(
    name="longproto",
    version="0.0.1",
    author="Victor Perron",
    author_email="victor@iso3103.net",
    description=("Long-polling prototype",),
    license="MIT",
    keywords="long polling",
    url="",
    packages=find_packages(exclude=['tests*']),
    long_description=read('README.md'),
    install_requires=[
        'requests-toolbelt',
        'aiohttp',
    ],

    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
    ],
    test_suite='',
    include_package_data=True,
)
