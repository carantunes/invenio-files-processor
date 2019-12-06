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

import pprint
import click
from flask import Flask, jsonify
from flask_babelex import Babel
from werkzeug.exceptions import BadRequest

from invenio_files_processor import InvenioFilesProcessor
from invenio_files_processor.errors import InvalidProcessor, ProcessorError
from invenio_files_processor.proxies import current_processors
from invenio_files_processor.views import blueprint

# Create Flask application
app = Flask(__name__)
Babel(app)
InvenioFilesProcessor(app)
app.register_blueprint(blueprint)

@app.cli.command()
@click.argument("processor_name")
@click.argument('file_path', type=click.Path(exists=True))
def process(processor_name, file_path):
    """Process file."""
    try:
        processor = current_processors.get_processor(processor_name)

        if not processor.can_process(file=file_path):
            raise InvalidProcessor(processor_name, file_path)

        results = processor.process(file=file_path)

        click.echo(pprint.pformat(results))
    except ProcessorError as exception:
        raise click.ClickException(exception)


@app.route('/process/<processor_name>/<file>')
def process(file, processor_name):
    """Process file."""
    file_path = 'data/{file}'.format(file=file)

    try:
        processor = current_processors.get_processor(processor_name)

        if not processor.can_process(file=file_path):
            return BadRequest(InvalidProcessor(processor_name, file_path))

        results = processor.process(file=file_path)

        return jsonify(results)
    except (ProcessorError, FileNotFoundError) as exception:
        raise BadRequest(exception)
