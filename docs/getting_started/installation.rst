Installation
============

Installing ``e2e-mobile``
-------------------------

``e2e-mobile`` is `available on PyPI (Python Package Index)
<https://pypi.org/project/e2e-mobile>`_. You can install with with ``pip``:

.. code-block:: console

   $ pip install --upgrade e2e-mobile

To check the version you installed:

.. code-block:: console

    $ e2e --version

Installing Appium
-----------------

Refer to this doc for the instructions: https://appium.io/docs/en/latest/quickstart/install.

TL;DR:

- Install ``node`` (via ``brew``) if not exists.
- Install ``appium`` (via ``npm``) if not exists.
- Install desired Appium drivers (via ``apium``) if not exists. The common choice is ``xcuitest`` for iOS and ``uiautomator2`` for Android.

The following commands demonstrate the steps above.

.. code-block:: console

    $ which npm &> /dev/null || brew install node
    $ appium --version &> /dev/null || npm install -g appium
    # For iOS
    $ (appium driver list --installed 2>&1 | grep xcuitest) || appium driver install xcuitest
    # For Android
    $ (appium driver list --installed 2>&1 | grep uiautomator2) || appium driver install uiautomator2
