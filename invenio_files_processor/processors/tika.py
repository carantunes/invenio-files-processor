# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Tika file processor."""

from __future__ import absolute_import, print_function

from flask import current_app
from invenio_files_rest.models import FileInstance, ObjectVersion
from invenio_files_rest.storage import FileStorage
from tika import unpack

from invenio_files_processor.processors.processor import FilesProcessor
from invenio_files_processor.processors.registry import ProcessorRegistry

# Tika configuration
READ_MODE_BINARY = 'rb'


class TikaProcessor(FilesProcessor):
    """Tika processor."""

    @staticmethod
    def id():
        """Tika identifier."""
        return ProcessorRegistry.Tika.value

    def _can_process(self, obj: ObjectVersion, **kwargs):
        """Check if given file can be processed."""
        return obj.file.readable

    def _process(self, obj: ObjectVersion, **kwargs):
        """Process the file with Tika."""
        file = obj.file  # type: FileInstance
        storage = file.storage(**kwargs)  # type: FileStorage
        fp = storage.open(mode=READ_MODE_BINARY)

        server_url = current_app.config['FILES_PROCESSOR_TIKA_SERVER_ENDPOINT']
        req_opts = current_app.config['FILES_PROCESSOR_TIKA_REQUEST_OPTIONS']

        try:
            result = unpack.from_file(
                fp,
                serverEndpoint=server_url,
                requestOptions=req_opts,
            )
        finally:
            fp.close()

        return result
