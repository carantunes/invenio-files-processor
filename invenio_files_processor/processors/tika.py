# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Tika file processor."""

from __future__ import absolute_import, print_function

import re

from invenio_files_rest.models import FileInstance, ObjectVersion
from invenio_files_rest.storage import FileStorage
from tika import parser

from invenio_files_processor.config import FILES_PROCESSOR_TIKA_SERVER_ENDPOINT
from invenio_files_processor.processors.processor import ProcessorInterface

# Tika configuration
TIKA_SERVER_ENDPOINT = FILES_PROCESSOR_TIKA_SERVER_ENDPOINT
TIKA_CLIENT_ONLY = True
READ_MODE_BINARY = 'rb'
PROCESSOR_ID = 'tika'


class TikaProcessor(ProcessorInterface):
    """Tika processor."""

    @staticmethod
    def id():
        return PROCESSOR_ID

    def _can_process(self, obj: ObjectVersion, **kwargs):
        """Check if given file can be processed."""
        return True

    def _process(self, obj: ObjectVersion, **kwargs):
        """Process the file with Tika."""
        file = obj.file  # type: FileInstance
        storage = file.storage(**kwargs)  # type: FileStorage
        fp = storage.open(mode=READ_MODE_BINARY)

        return parser.from_file(fp)
