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
        return f"Processor {self.processor} is already registered."


class UnsupportedProcessor(ProcessorError):
    """Processor is not supported."""

    def __str__(self):
        return f"Processor {self.processor} is not supported."


class InvalidProcessor(ProcessorError):
    """Processor is not registered."""

    def __init__(self, processor, file):
        """Initialize exception."""
        self.file = file
        super().__init__(processor)

    def __str__(self):
        return f"Processor {self.processor} " \
               f"can't be applied to file {self.file}."
