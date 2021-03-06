#!/usr/bin/env python
# Learn more: https://github.com/kennethreitz/setup.py

import os
import sys

from codecs import open

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

# pyOpenSSL version 18.0.0 dropped support for Python 2.6
if sys.version_info < (2, 7):
    PYOPENSSL_VERSION = 'pyOpenSSL >= 0.14, < 18.0.0'
else:
    PYOPENSSL_VERSION = 'pyOpenSSL >= 0.14'

install_requires = [
    'chardet>=3.0.2,<3.1.0',
    'idna>=2.5,<2.8',
    'urllib3>=1.24.2',
    'certifi>=2017.4.17',
    'camel_snake_kebab==0.3.2',
    'jiphy>=1.2.2',
    'dill>=0.2.8.2',
    'yapf>=0.25.0']
test_requirements = [
    'pytest-httpbin==0.0.7',
    'pytest-cov',
    'slimit>=0.8.1',
    'yapf>=0.22.0',
    'pytest-mock',
    'pytest-xdist',
    'PySocks>=1.5.6,!=1.5.7',
    'pytest>=2.8.0']

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='slayer',
    version='0.0.1',
    description='Spatial plots in Python',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author='Andrew Duberstein',
    author_email='ajduberstein+slayer@gmail.com',
    url='https://github.com/ajduberstein/slayer',
    keywords=['data', 'geospatial', 'visualization'],
    download_url='https://github.com/ajduberstein/slayer/releases/download/0.0.1/slayer-0.0.1.tar.gz',
    packages=find_packages(exclude=['example*']),
    include_package_data=True,
    package_dir={'slayer': 'slayer'},
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=install_requires,
    license='MIT',
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
    extras_require={
        'security': [PYOPENSSL_VERSION, 'cryptography>=1.3.4', 'idna>=2.0.0'],
        'socks': ['PySocks>=1.5.6, !=1.5.7'],
        'socks:sys_platform == "win32" and (python_version == "2.7" or python_version == "2.6")': ['win_inet_pton'],
    },
)
