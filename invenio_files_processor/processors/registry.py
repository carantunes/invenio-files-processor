# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.
"""Processors Registry."""

from enum import Enum


class ProcessorRegistry(Enum):
    """Processors Registry enum."""

    Tika = 'tika'
