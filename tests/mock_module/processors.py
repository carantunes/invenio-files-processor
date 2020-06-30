# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Dummy processor."""

from __future__ import absolute_import, print_function

from invenio_files_rest.models import FileInstance, ObjectVersion

from invenio_files_processor.processors.processor import FilesProcessor


class DummyProcessor(FilesProcessor):
    """Dummy processor."""

    @staticmethod
    def id():
        """Dummy identifier."""
        return 'dummy'

    def _can_process(self, obj: ObjectVersion, **kwargs):
        """Check if given file can be processed."""
        can_process = kwargs.get('can_process',  True)

        return can_process

    def _process(self, obj: ObjectVersion, **kwargs):
        """Process the file with Dummy."""
        file = obj.file  # type: FileInstance

        return dict(content="dummy")
