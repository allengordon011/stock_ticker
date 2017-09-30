#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'flask',
    Flask-SQLAlchemy==2.1,
]

setup_requirements = [
    # TODO(allengordon011): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='stock_ticker',
    version='0.1.0',
    description="A simple stock ticker website for building a list of stocks and displaying a simple ticker of the list of stocks.",
    long_description=readme + '\n\n' + history,
    author="Allen Gordon",
    author_email='allengordon011@gmail.com',
    url='https://github.com/allengordon011/stock_ticker',
    packages=find_packages(include=['stock_ticker']),
    entry_points={
        'console_scripts': [
            'stock_ticker=stock_ticker.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='stock_ticker',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
