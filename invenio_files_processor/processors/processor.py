# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Abstract class file processor."""
import errno
from abc import ABC, abstractmethod
from os import strerror

from flask import current_app
from invenio_files_rest.models import FileInstance, ObjectVersion

from invenio_files_processor.errors import InvalidProcessor
from invenio_files_processor.signals import file_processed


class ProcessorInterface(ABC):
    """Generic processor interface."""

    def process(self, obj: ObjectVersion, **kwargs):
        """Process the file."""
        ProcessorInterface.check_valid_file(obj)

        if not self._can_process(obj=obj, **kwargs):
            raise InvalidProcessor(self.id(), obj.basename)

        data = self._process(obj=obj, **kwargs)

        file_processed.send(
            current_app._get_current_object(),
            processor_id=self.id(),
            file=obj,
            data=data,
        )

        return data

    @staticmethod
    def check_valid_file(obj: ObjectVersion):
        """Check if file is valid."""
        is_valid = (
            isinstance(obj, ObjectVersion)
            and isinstance(obj.file, FileInstance)
        )

        if not is_valid:
            raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT))

    @staticmethod
    @abstractmethod
    def id():
        """Specific processor identifier."""
        pass

    @abstractmethod
    def _can_process(self, obj: ObjectVersion, **kwargs):
        """Specific implementation of validation of file can be processed."""
        pass

    @abstractmethod
    def _process(self, obj: ObjectVersion, **kwargs):
        """Specific implementation of file processing."""
        pass
