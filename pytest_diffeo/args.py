"""Command-line arguments for tests.

This enables some common command-line arguments:

``--runslow``
  Run tests flagged with @pytest.fixture.slow
``--runperf``
  Run tests flagged with @pytest.fixture.performance
``--redis-address``
  hostname:portnumber for a Redis instance

-----

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.

"""

from __future__ import absolute_import
import os.path
import pytest

def pytest_addoption(parser):
    group = parser.getgroup('test selection')
    group.addoption('--runslow', action='store_true',
                    help='run known-slow tests')
    group.addoption('--runperf', action='store_true',
                    help='run performance tests')
    group.addoption('--runload', action='store_true',
                    help='run load tests')

    group = parser.getgroup('external dependencies')
    group.addoption('--redis-address', metavar='HOST:PORT',
                     help='location of a Redis database server')
    group.addoption('--test-data-dir', metavar='TEST-DATA-DIRECTORY',
                     default='/opt/diffeo/data', action="store",
                     help='location of test data directory')

def pytest_configure(config):
    # Declare our markers
    config.addinivalue_line('markers',
                            'slow: mark tests as taking longer than '
                            'your average unit test')
    config.addinivalue_line('markers',
                            'performance: mark tests as performance tests')
    config.addinivalue_line('markers',
                            'load: mark tests as load tests')

def pytest_runtest_setup(item):
    pairs = [('slow', 'slow'),
             ('perf', 'performance'),
             ('load', 'load')]
    for option, marker in pairs:
        run = '--run{}'.format(option)
        if marker in item.keywords and not item.config.getoption(run):
            pytest.skip('need {} option to run'.format(run))

@pytest.fixture(scope='session')
def redis_address(request):
    addr = request.config.getoption('--redis-address')
    assert addr is not None, \
        "this test requires --redis-address on the command line"
    return addr

@pytest.fixture(scope='session')
def test_data_dir(request):
    test_data_dir = request.config.getoption('--test-data-dir')
    assert os.path.exists(test_data_dir), \
        "Directory with test directory must exist"
    return test_data_dir
