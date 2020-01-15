# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Minimal Flask application example.

SPHINX-START

First install Invenio-Files-Processor, setup the application and load
fixture data by running:

.. code-block:: console

   $ pip install -e .[all]
   $ cd examples
   $ ./app-setup.sh
   $ ./app-fixtures.sh

Next, start the development server:

.. code-block:: console

   $ FLASK_DEBUG=1 FLASK_APP=app.py flask run -p 5000

and open the example application in your browser:

.. code-block:: console

    $ open http://127.0.0.1:5000/process/tika/sample.pdf

Alternatively run de cli:

.. code-block:: console

   $ FLASK_DEBUG=1 FLASK_APP=app.py flask process tika data/sample.pdf

.. code-block:: console

To reset the example application run:

.. code-block:: console

    $ ./app-teardown.sh

SPHINX-END
"""

from __future__ import absolute_import, print_function

import os
import pprint
import shutil
from os.path import dirname, exists, join

import click
from flask import Flask, current_app, jsonify
from flask_babelex import Babel
from invenio_db import InvenioDB, db
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Bucket, FileInstance, Location, \
    MultipartObject, ObjectVersion, Part
from invenio_logging.console import InvenioLoggingConsole
from werkzeug.exceptions import BadRequest

from invenio_files_processor import InvenioFilesProcessor
from invenio_files_processor.errors import ProcessorError
from invenio_files_processor.proxies import current_processors
from invenio_files_processor.signals import file_processed

BUCKET_SAMPLE = '00000000-0000-0000-0000-000000000000'
SAMPLE_DIR = 'data/'


def allow_all(*args, **kwargs):
    """Return permission that always allow an access.
    :returns: A object instance with a ``can()`` method.
    """
    return type('Allow', (), {'can': lambda self: True})()


def file_processed_action(app, processor_id: str, file: ObjectVersion, data):
    current_app.logger.info(
        "Processor {id} finished processing file {file} with status {status}".
        format(
            id=processor_id,
            file=file,
            status=data['status']
        )
    )


# Create Flask application
app = Flask(__name__)
app.config.update(dict(
    BROKER_URL='redis://',
    CELERY_RESULT_BACKEND='redis://',
    DATADIR=join(dirname(__file__), 'instance/fs'),
    FILES_REST_MULTIPART_CHUNKSIZE_MIN=4,
    REST_ENABLE_CORS=True,
    SECRET_KEY='CHANGEME',
    SQLALCHEMY_ECHO=False,
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///instance/test.db'
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    FILES_REST_PERMISSION_FACTORY=allow_all,
))

Babel(app)
InvenioFilesProcessor(app)
InvenioDB(app)
InvenioFilesREST(app)
InvenioLoggingConsole(app)

file_processed.connect(file_processed_action)


@app.cli.group()
def fixtures():
    """Command for working with sample data."""


@fixtures.command()
def files():
    """Load files."""
    d = current_app.config['DATADIR']

    if exists(d):
        shutil.rmtree(d)
    os.makedirs(d)

    # Clear data
    Part.query.delete()
    MultipartObject.query.delete()
    ObjectVersion.query.delete()
    Bucket.query.delete()
    FileInstance.query.delete()
    Location.query.delete()
    db.session.commit()

    # Create location
    loc = Location(name='default', uri=d, default=True)
    db.session.add(loc)
    db.session.commit()

    # Bucket
    b1 = Bucket.create(loc)
    b1.id = BUCKET_SAMPLE
    for f in os.listdir(SAMPLE_DIR):
        with open(join(SAMPLE_DIR, f), 'rb') as fp:
            ObjectVersion.create(b1, f, stream=fp)

    db.session.commit()


@app.cli.command()
@click.argument("processor_name")
@click.argument('file_name')
def process(processor_name, file_name):
    """Process file."""
    file = ObjectVersion.get(BUCKET_SAMPLE, file_name)

    try:
        processor = current_processors.get_processor(processor_name)

        results = processor.process(obj=file)

        click.echo(pprint.pformat(results))
    except ProcessorError as exception:
        raise click.ClickException(exception)


@app.route('/process/<processor_name>/<file_name>')
def process(file_name, processor_name):
    """Process file."""
    file = ObjectVersion.get(BUCKET_SAMPLE, file_name)

    try:
        processor = current_processors.get_processor(processor_name)

        result = processor.process(obj=file)

        return jsonify(result)
    except (ProcessorError, FileNotFoundError) as exception:
        raise BadRequest(exception)
