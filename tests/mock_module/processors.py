# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Dummy processor."""

from invenio_files_rest.models import FileInstance, ObjectVersion

from invenio_files_processor.processors.processor import FilesProcessor


class DummyProcessor(FilesProcessor):
    """Dummy processor."""

    id = 'dummy'

    def can_process(self, obj, **kwargs):
        """Check if given file can be processed."""
        can_process = kwargs.get('can_process',  True)

        return can_process

    def process_file(self, obj, **kwargs):
        """Process the file with Dummy."""
        file = obj.file

        return dict(content="dummy")
