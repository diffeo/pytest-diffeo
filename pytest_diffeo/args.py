"""Command-line arguments for tests.

This enables some common command-line arguments:

``--runslow``
  Run tests flagged with @pytest.fixture.slow
``--runperf``
  Run tests flagged with @pytest.fixture.performance
``--run-go-ingest-pipeline``
  Run tests flagged with @pytest.fixture.go_ingest_pipeline
``--redis-address``
  hostname:portnumber for a Redis instance
``--profile outfile``
  log profiling data per test to outfile
``--profile-truncate``
  clobber any old profiling out file at start of run
``--elastic-address``
  hostname:portnumber for an Elasticsearch instance

-----

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.

"""

from __future__ import absolute_import
import logging
import os.path
import pstats
import time


try:
    import cProfile as profile
except:
    import profile

import pytest
from six import StringIO


def pytest_addoption(parser):
    group = parser.getgroup('test selection')
    group.addoption('--runslow', action='store_true',
                    help='run known-slow tests')
    group.addoption('--runperf', action='store_true',
                    help='run performance tests')
    group.addoption('--runload', action='store_true',
                    help='run load tests')
    group.addoption('--run-integration', action='store_true',
                    help='run integration tests')
    group.addoption('--run-go-ingest-pipeline', action='store_true',
                    help='run tests that use the Go ingest pipeline')

    group = parser.getgroup('external systems')
    group.addoption('--elastic-address', metavar='HOST:PORT',
                    help='location of an ElasticSearch database server')
    group.addoption('--redis-address', metavar='HOST:PORT',
                    help='location of a Redis database server')
    group.addoption('--third-dir', metavar='THIRD-DIR',
                    help='location of a third party software')

    group = parser.getgroup('general')
    group.addoption('--profile', metavar='path',
                    help='run tests with profiling, write results to file')
    group.addoption('--profile-truncate', action='store_true', default=False,
                    help='when profiling, truncate output file at start')
    group.addoption('--log-level', metavar='DEBUG|INFO|WARNING|ERROR|FATAL',
                    default='DEBUG',
                    help='Control logging level of tests.')


def pytest_configure(config):
    # Declare our markers
    config.addinivalue_line('markers',
                            'slow: mark tests as taking longer than '
                            'your average unit test')
    config.addinivalue_line('markers',
                            'performance: mark tests as performance tests')
    config.addinivalue_line('markers',
                            'load: mark tests as load tests')
    config.addinivalue_line('markers',
                            'integration: mark tests as integration tests')

    if config.getoption('profile_truncate'):
        profile_outpath = config.getoption('profile')
        if profile_outpath:
            fout = open(profile_outpath, 'w')
            fout.truncate(0)
            fout.close()


def pytest_runtest_setup(item):
    pairs = [
        ('slow', 'slow'),
        ('perf', 'performance'),
        ('load', 'load'),
        ('-integration', 'integration'),
        ('-go-ingest-pipeline', 'go_ingest_pipeline'),
    ]
    for option, marker in pairs:
        run = '--run{0}'.format(option)
        if marker in item.keywords and not item.config.getoption(run):
            pytest.skip('need {0} option to run'.format(run))

    profile_outpath = item.config.getoption('profile')
    if profile_outpath:
        prof = profile.Profile()
        prof.enable()
        item.profiler = prof

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, item.config.getoption('log_level')))


def pytest_runtest_teardown(item, nextitem):
    profile_outpath = item.config.getoption('profile')
    if profile_outpath:
        prof = getattr(item, 'profiler', None)
        if prof:
            prof.disable()
            # build blob to write one-shot to beat thread interleaving.
            fout = StringIO()
            fout.write(
                '\n{0} {1}\n'.format(time.strftime('%Y%m%d_%H%M%S'), item))
            ps = pstats.Stats(prof, stream=fout)
            ps.sort_stats('cumulative', 'calls')
            ps.print_stats()
            fout.write('\n\tfunction callers\n')
            ps.print_callers()
            fout.write('\n\tfunction callees\n')
            ps.print_callees()
            ff = open(profile_outpath, 'a')
            ff.write(fout.getvalue())
            ff.close()


@pytest.fixture(scope='session')
def redis_address(request):
    '''network address for a redis server to be used by tests
    '''
    addr = request.config.getoption('--redis-address')
    if addr is None:
        host = os.environ.get('REDIS_PORT_6379_TCP_ADDR', None)
        port = os.environ.get('REDIS_PORT_6379_TCP_PORT', None)
        if host and port:
            addr = host + ':' + port
    assert addr is not None, \
        "this test requires --redis-address on the command line"
    return addr


@pytest.fixture(scope='session')
def elastic_address(request):
    'network address for an ElasticSearch server to be used by tests'
    addr = request.config.getoption('--elastic-address')
    if addr is None:
        host = os.environ.get('ELASTICSEARCH_PORT_9200_TCP_ADDR', None)
        port = os.environ.get('ELASTICSEARCH_PORT_9200_TCP_PORT', None)
        if host and port:
            addr = host + ':' + port
    assert addr is not None, \
        "this test requires --elastic-address on the command line"
    return addr


@pytest.fixture(scope='session')
def third_dir(request):
    '''directory containing third-party software, such as NLP taggers
    '''
    third_dir = request.config.getoption('--third-dir')
    assert third_dir is not None, \
        "this test requires --third_dir on the command line"
    assert os.path.exists(third_dir), "Directory must exist"
    return third_dir
