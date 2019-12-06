# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Proxy for current files processor."""

from __future__ import absolute_import, print_function

from flask import current_app
from werkzeug.local import LocalProxy


def _get_current_processors():
    """Return current state of the processors extension."""
    return current_app.extensions['invenio-files-processor']


current_processors = LocalProxy(_get_current_processors)
