"""Support code for py.test tests.

This module includes support code that defines common command-line options
and provides other common infrastructure for tests.

-----

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.

"""

from __future__ import absolute_import

from pytest_diffeo.args import pytest_addoption, pytest_configure, \
    pytest_runtest_setup, \
    pytest_runtest_teardown, \
    third_dir, \
    redis_address, \
    ingest_v2, \
    elastic_address
from pytest_diffeo.namespace import make_namespace_string, namespace_string
