#!/usr/bin/env sh
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CERN.
#
# Invenio-Files-Processor is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

pip install -e .[all]
cd examples
sh app-setup.sh
sh app-fixtures.sh
export FLASK_APP=app.py
flask run
