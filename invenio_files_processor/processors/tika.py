# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Tika file processor."""

from __future__ import absolute_import, print_function

from tika import parser
from invenio_files_processor.config import FILES_PROCESSOR_TIKA_SERVER_ENDPOINT
from invenio_files_processor.processors.processor import ProcessorInterface

# Tika configuration
TIKA_SERVER_ENDPOINT = FILES_PROCESSOR_TIKA_SERVER_ENDPOINT
TIKA_CLIENT_ONLY = True


class TikaProcessor(ProcessorInterface):
    """Tika processor."""

    @staticmethod
    def can_process(file, *args, **kwargs):
        """Check if given file can be processed."""
        ProcessorInterface.check_valid_file(file)

        return True

    @staticmethod
    def process(file, *args, **kwargs):
        """Process the file with Tika."""
        ProcessorInterface.check_valid_file(file)

        parsed = parser.from_file(file)

        return parsed
