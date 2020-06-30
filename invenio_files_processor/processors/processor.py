# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
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

from ..errors import InvalidProcessor
from ..signals import file_processed


class FilesProcessor(ABC):
    """Generic processor interface."""

    def process(self, obj, **kwargs):
        """Process the file.

        :param obj: ObjectVersion file input
        :return: Processing result
        """
        print(obj)
        self.check_valid_file(obj)

        if not self.can_process(obj=obj, **kwargs):
            raise InvalidProcessor(self.id, obj.basename)

        data = self.process_file(obj=obj, **kwargs)

        file_processed.send(
            current_app._get_current_object(),
            processor_id=self.id,
            file=obj,
            data=data,
        )

        return data

    @staticmethod
    def check_valid_file(obj):
        """Check if file is valid."

        :param obj: ObjectVersion file input
        """
        is_valid = (
            isinstance(obj, ObjectVersion)
            and isinstance(obj.file, FileInstance)
        )

        if not is_valid:
            raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT))

    @property
    @abstractmethod
    def id(self):
        """Specific processor identifier."""
        pass

    @abstractmethod
    def can_process(self, obj, **kwargs):
        """Specific implementation of validation of file can be processed.

        :param obj: ObjectVersion file input
        """
        pass

    @abstractmethod
    def process_file(self, obj, **kwargs):
        """Specific implementation of file processing.

        :param obj: ObjectVersion file input
        """
        pass
