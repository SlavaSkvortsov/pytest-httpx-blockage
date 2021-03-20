from io import open
from typing import List

from setuptools import setup

import pytest_httpx_blockage


def get_readme() -> str:
    """read the contents of the README file"""
    with open('README.md', encoding='utf-8') as f:
        return f.read()


def get_requirements() -> List[str]:
    """read the contents of the requirements file"""
    with open('requirements.txt', encoding='utf-8') as f:
        return [line.replace('==', '>=') for line in f.readlines()]


setup(
    name='pytest-httpx-blockage',
    version=pytest_httpx_blockage.__version__,
    setup_requires=['better-setuptools-git-version'],
    install_requires=get_requirements(),
    tests_require=[],
    packages=['pytest_httpx_blockage'],
    package_data={'pytest_httpx_blockage': ['py.typed']},
    entry_points={'pytest11': ['blockage-httpx = pytest_httpx_blockage.plugin']},
    include_package_data=True,
    author='Slava Skvortsov',
    description='Disable httpx requests during a test run',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/SlavaSkvortsov/pytest-httpx-blockage',
    zip_safe=True,
    classifiers=[
        'Framework :: Pytest',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
