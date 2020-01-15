# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for files' processing and or transforming."""

import os

from setuptools import find_packages, setup

from invenio_files_processor.processors.registry import ProcessorRegistry

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.3.3',
    'pydocstyle>=2.0.0',
    'pytest-cov>=2.5.1',
    'pytest-pycodestyle>=2.0.0',
    'pytest-invenio>=1.0.5',
    'mock>=3.0.5',
    'invenio-db>=1.0.4'
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    # tika processor
    'tika': [
        # 'tika==1.24',
        # TODO: uncomment after
        #  https://github.com/chrismattmann/tika-python/pull/240 is released
        'tika @ git+https://github.com/prough21/tika-python@5cf3452887b2a0a181387548d360d3503f6713dc#egg=tika'
    ],
    'tests': tests_require,
    'all': [
    ]
}

for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'Flask-BabelEx>=0.9.3',
    'blinker>=1.4',
    'invenio-files-rest>=1.0.6',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_files_processor', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-files-processor',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio TODO',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-files-processor',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_files_processor = '
            'invenio_files_processor:InvenioFilesProcessor',
        ],
        'invenio_files_processor': [
            '{tika} = invenio_files_processor.processors.tika:TikaProcessor'.
            format(tika=ProcessorRegistry.Tika.value)
        ]
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 1 - Planning',
    ],
)
