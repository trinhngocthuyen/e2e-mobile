End-to-end Testing Package for Mobile Apps
==========================================

.. _readthedocs: https://e2e-mobile.readthedocs.io
.. _contributing guidelines: https://e2e-mobile.readthedocs.io/en/latest/contributing.html
.. _FAQ: https://e2e-mobile.readthedocs.io/en/latest/faq.html#python-setup

.. image:: https://img.shields.io/pypi/v/e2e-mobile.svg
    :target: https://pypi.org/project/e2e-mobile

.. image:: https://img.shields.io/pypi/l/e2e-mobile.svg
    :target: https://github.com/trinhngocthuyen/e2e-mobile/blob/main/LICENSE

``e2e-mobile`` is a Python package providing convenient setup for end-to-end testing in mobile apps. This package is the combined magic of Appium and Pytest. It helps us:

- Write tests once, for both platforms (iOS & Android).
- Write reusable & readable tests that can scale to support complex use cases.

.. image:: _static/recording.gif

What does a test with this framework look like?
-----------------------------------------------

.. code-block:: python

    from e2e_ext.core.tester import Tester

    def test_tutorial(tester: Tester):
        tester.ui.home.skip_tutorial()
        tester.relaunch_app()
        tester.ui.home.must_not_see_tutorial()

    def test_settings(tester: Tester):
        tester.ui.home.skip_tutorial()
        tester.ui.home.go_to_settings()
        tester.ui.settings.swipe('up')
        tester.ui.settings.element('About the app').must_exist()
        tester.ui.settings.swipe('down')
        tester.ui.settings.close()

`Get started with e2e-mobile now! <https://e2e-mobile.readthedocs.io/en/latest/getting_started/index.html>`_

Installation
------------

``e2e-mobile`` is `available on PyPI (Python Package Index)
<https://pypi.org/project/e2e-mobile>`_. You can install with with ``pip``:

.. code-block:: console

   $ pip install --upgrade e2e-mobile

First time hearing ``pip``? Check this `FAQ`_.

Usage
-----

Kindly check out the related docs on readthedocs_:

- `Getting Started <https://e2e-mobile.readthedocs.io/en/latest/getting_started/index.html>`_

Documentation
-------------

Kindly check out the related docs on readthedocs_:

- `API Reference <https://e2e-mobile.readthedocs.io/en/latest/api/reference.html>`_

Contributing
------------

Refer to the `contributing guidelines`_ for how to contribute to this project.
