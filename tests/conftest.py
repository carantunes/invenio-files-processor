# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

from __future__ import absolute_import, print_function

import os

import pytest
from flask import Flask
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Bucket, ObjectVersion
from pkg_resources import EntryPoint
from six import BytesIO
from tests.mock_module.processors import DummyProcessor, TestRegistry

from invenio_files_processor import InvenioFilesProcessor
from invenio_files_processor.proxies import current_processors


@pytest.fixture()
def app():
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            'sqlite:///:memory:'),
        WTF_CSRF_ENABLED=False,
        SERVER_NAME='invenio.org',
        SECRET_KEY='TEST_SECRET_KEY',
    )

    InvenioFilesREST(app)
    InvenioFilesProcessor(app)

    with app.app_context():
        yield app


@pytest.fixture()
def dummy_app(app):
    """Dummy application fixture."""
    current_processors.register_processor(
        DummyProcessor.id(),
        DummyProcessor,
    )


def mock_iter_entry_points_factory(data, mocked_group):
    """Create a mock iter_entry_points function."""
    from pkg_resources import iter_entry_points

    def entrypoints(group, name=None):
        if group == mocked_group:
            for entrypoint in data:
                yield entrypoint
        else:
            for x in iter_entry_points(group=group, name=name):
                yield x

    return entrypoints


@pytest.fixture()
def processor_entrypoints():
    """Entrypoint fixture."""
    eps = []
    event_type_name = TestRegistry.Dummy
    entrypoint = EntryPoint(event_type_name, event_type_name)
    entrypoint.load = lambda: lambda: DummyProcessor
    eps.append(entrypoint)

    return mock_iter_entry_points_factory(eps, 'invenio_files_processor')


@pytest.fixture()
def bucket(database, location):
    """File system location."""
    b1 = Bucket.create()
    b1.id = '00000000-0000-0000-0000-000000000000'
    database.session.commit()
    return b1


@pytest.fixture()
def objects(database, bucket):
    """Multipart object."""
    content = b'some content'
    obj = ObjectVersion.create(
        bucket,
        'test.pdf',
        stream=BytesIO(content),
        size=len(content)
    )
    database.session.commit()
    return obj
