# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Abstract class file processor."""
import errno
from os import strerror
from os.path import isfile
from abc import ABC, abstractmethod


class ProcessorInterface(ABC):
    """Generic processor interface."""

    @staticmethod
    def check_valid_file(filename):
        if not isfile(filename):
            raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT), filename)

    @abstractmethod
    def can_process(self, file, *args, **kwargs):
        """Check if given file can be processed."""
        pass

    @abstractmethod
    def process(self, file, *args, **kwargs):
        """Process the file."""
        pass

