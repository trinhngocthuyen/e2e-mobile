Quick Start
===========

Initialize the project
----------------------

Run the following command to kick off the initial setup.

.. code-block:: console

    $ e2e init

The command above generates the example code needed including:

- ``e2e_ext`` directory: where you write extensions (UI assertions, simulations...).
- ``tests`` directory: where you write your tests.

Recommended ``.gitignore`` settings
-----------------------------------

While executing tests, ``e2e-mobile`` writes some data which might be useful for troubleshooting issues. You are recommended to add the following paths to ``.gitignore``.

.. code-block:: console

    # In your .gitignore file
    tmp/apps/
    .artifacts/

Running the example tests
-------------------------

This package offers a convenient way to try out the example tests.

First, you need to build an app for testing and obtain the ``.app`` bundle.
No worries, you simply need to run:

.. code-block:: console

    $ e2e demo build

This command clones the `Wikipedia iOS project <https://github.com/wikimedia/wikipedia-ios>`_, builds it, and place the ``.app`` bundle under ``tmp/apps/Wikipedia.zip``.

.. note::

    This tool builds the Wikipedia iOS project using ``xcodebuild``. In case you are not familiar with iOS development, you need to install Xcode and properly configure ``xcode-select``:

    .. code-block:: console

        $ sudo xcode-select -s /Applications/Xcode.app

Then, you can run the example tests:

.. code-block:: console

    $ pytest tests/e2e/test_example.py

Remember to open the Simulator app to see what's going on. You should see the test execution like this:

.. image:: ../../_static/recording.gif
