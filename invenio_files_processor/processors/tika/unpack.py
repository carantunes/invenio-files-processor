# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Tika file processor."""

from flask import current_app
from invenio_files_rest.models import FileInstance, ObjectVersion
from invenio_files_rest.storage import FileStorage
from tika import unpack

from ..processor import FilesProcessor

# Tika configuration
READ_MODE_BINARY = 'rb'


class UnpackProcessor(FilesProcessor):
    """Tika processor."""

    id = 'tika_unpack'

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
