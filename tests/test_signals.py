# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Test file signals."""
from invenio_files_rest.models import ObjectVersion
from tests.mock_module.processors import DummyProcessor

from invenio_files_processor.proxies import current_processors
from invenio_files_processor.signals import file_processed


def test_signals(dummy_app, objects):
    """Test file_processed signal."""
    obj = ObjectVersion.get('00000000-0000-0000-0000-000000000000', 'test.pdf')

    calls = []

    def file_processed_listener(app, processor_id, file, data):
        assert processor_id == DummyProcessor.id()
        assert obj == file
        assert data['content'] == 'dummy'

        calls.append("file-processed")

    file_processed.connect(file_processed_listener, weak=False)

    try:
        processor = current_processors.get_processor(name=DummyProcessor.id())

        processor.process(obj=obj)

        assert calls == ["file-processed"]
    finally:
        file_processed.disconnect(file_processed_listener)
