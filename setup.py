#!/usr/bin/env python
"""
Package metadata for edx-milestones.
"""
import os
import re
import sys

from setuptools import find_packages, setup

from milestones import __version__ as VERSION


def get_version(*file_paths):
    """
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    with open(filename, encoding='utf-8') as _fp:
        version_file = _fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.

    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        requirements.update(
            line.split('#')[0].strip()
            for line in open(path, encoding='utf-8').readlines()  # pylint: disable=consider-using-with
            if is_requirement(line.strip())
        )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.

    Returns:
        bool: True if the line is not blank, a comment, a URL, or an included file
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))


if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a v{VERSION} -m 'version {VERSION}'")
    os.system("git push --tags")
    sys.exit()

setup(
    name='edx-milestones',
    version=VERSION,
    description='Significant events module for Open edX',
    long_description=open('README.md', encoding='utf-8').read(),  # pylint: disable=consider-using-with
    long_description_content_type="text/markdown",
    author='edX',
    url='https://github.com/openedx/edx-milestones',
    license='AGPL',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.2',
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=load_requirements('requirements/base.in'),
    tests_require=load_requirements('requirements/test.in')
)
