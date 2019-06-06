#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals
from setuptools import setup, find_packages
from milestones import __version__ as VERSION

setup(
    name='edx-milestones',
    version=VERSION,
    description='Significant events module for Open edX',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='edX',
    url='https://github.com/edx/edx-milestones',
    license='AGPL',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "django>=1.8,<2.0",
        "django-model-utils",
        "edx-opaque-keys>=0.2.1,<1.0.0",
        "six",
    ],
    tests_require=[
        "coverage==4.5.3",
        "nose==1.3.3",
        "httpretty==0.8.0",
        "pep8==1.5.7",
        "pylint==1.2.1",
        "pep257==0.3.2"
    ]
)
