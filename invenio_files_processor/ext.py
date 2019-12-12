# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for files' processing and or transforming."""

from __future__ import absolute_import, print_function

import pkg_resources

from invenio_files_processor.errors import DuplicatedProcessor, \
    UnsupportedProcessor

from . import config


class _InvenioFilesProcessorState(object):
    """Store registered processors."""

    def __init__(
        self,
        app,
        entry_point_group=None,
        **kwargs
    ):
        """Initialize state.

        :param app: An instance of :class:`~flask.app.Flask`.
        :param entry_point_group: The entrypoint group name to load processors.
        """
        self.app = app
        self.entry_point_group = entry_point_group
        self.processors = {}

        if entry_point_group:
            self._load_entry_point_group(entry_point_group)

    def _load_entry_point_group(self, entry_point_group):
        """Load processors from an entry point group."""
        for ep in pkg_resources.iter_entry_points(group=entry_point_group):
            self.register_processor(ep.name, ep.load())

    def register_processor(self, name, processor):
        """Register a processor."""
        if name in self.processors:
            raise DuplicatedProcessor(name)
        self.processors[name] = processor()

    def get_processor(self, processor_name=None):
        """Get processor."""
        try:
            return self.processors[processor_name]
        except KeyError:
            raise UnsupportedProcessor(processor_name)


class InvenioFilesProcessor(object):
    """Invenio-Files-Processor extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(
        self,
        app,
        entry_point_group='invenio_files_processor',
        **kwargs
    ):
        """Flask application initialization.

        :param app: An instance of :class:`~flask.app.Flask`.
        :param entry_point_group:
        """
        self.init_config(app)

        state = _InvenioFilesProcessorState(
            app,
            entry_point_group=entry_point_group,
            **kwargs
        )
        app.extensions['invenio-files-processor'] = state

        return state

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('FILES_PROCESSOR_'):
                app.config.setdefault(k, getattr(config, k))
