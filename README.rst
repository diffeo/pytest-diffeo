pytest-diffeo
=============

Common py.test support for Diffeo tests.

If this package is installed, then you can run ``py.test`` with additional
command-line arguments ``--runperf``, ``--runslow``, ``-runload``, or ``-run-integration``.
Tests marked with ``@pytest.mark.performance``, ``@pytest.mark.slow``,
``@pytest.mark.load``, and ``pytest.mark.integration`` respectively, will not
be run unless the corresponding command-line option is present.

This package also provides a ``redis_address`` fixture to get the
location of an external Redis installation.  This must be provided via
a ``--redis-address`` command-line argument.
