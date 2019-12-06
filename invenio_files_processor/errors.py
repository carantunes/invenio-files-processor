# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Processor errors."""


class ProcessorError(Exception):
    """Base class for Processor errors."""

    def __init__(self, processor):
        """Initialize exception."""
        self.processor = processor


class DuplicatedProcessor(ProcessorError):
    """Processor is already registered."""

    def __str__(self):
        return "Processor {0} is already registered.".format(self.processor)


class UnsupportedProcessor(ProcessorError):
    """Processor is not supported."""

    def __str__(self):
        return "Processor {0} is not supported.".format(self.processor)


class InvalidProcessor(ProcessorError):
    """Processor is not registered."""

    def __init__(self, processor, file):
        """Initialize exception."""
        self.file = file
        super().__init__(processor)

    def __str__(self):
        return "Processor {0} can not be applied to file.".format(
            self.processor,
            self.file
        )
