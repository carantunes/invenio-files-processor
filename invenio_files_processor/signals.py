# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Signals for Invenio-Files-Processor."""

from __future__ import absolute_import, print_function

from blinker import Namespace

_signals = Namespace()

file_processed = _signals.signal('file-processed')
"""File processed signal.
Sent when a file is processed.
"""
