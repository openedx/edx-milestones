#!/usr/bin/env python

from setuptools import setup

setup(
    name='edx-milestones',
    version='0.1.1',
    description='Significant events module for Open edX',
    author='edX',
    url='https://github.com/edx/edx-milestones',
    license='AGPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages=['milestones'],
    dependency_links=[
    ],
    install_requires=[
    ]
)
