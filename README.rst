pytest-diffeo
=============

Common py.test support for Diffeo tests.

If this package is installed, then you can run ``py.test`` with additional
command-line arguments ``--runperf``, ``--runslow``, or ``-runload``.
Tests marked with ``@pytest.mark.performance``, ``@pytest.mark.slow``,
and ``@pytest.mark.load``, respectively, will not be run unless the
corresponding command-line option is present.

This package also provides a ``redis_address`` fixture to get the
location of an external Redis installation.  This must be provided via
a ``--redis-address`` command-line argument.
