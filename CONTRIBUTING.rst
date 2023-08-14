Contributing
============

.. _autoflake: https://github.com/PyCQA/autoflake
.. _isort: https://github.com/PyCQA/isort
.. _black: https://github.com/psf/black

You are more than welcome to contribute to the project in various ways:

- Implement features
- Fix bugs
- Write tests
- Write documentation

The following section describes the development workflow when contributing to the project.

Development Workflow
--------------------

**Step 1: Clone the project**

**Step 2: Install dependencies**

.. code-block:: console

    $ make install

This step install necessary dependencies and creates a virtual environment (in ``.venv`` directory).

To install Appium related dependencies, simply run:

.. code-block:: console

    $ make bootstrap

**Step 3: Activate virtual environment**

.. code-block:: console

    $ source .venv/bin/activate

**Step 4: Make changes**

To try out e2e tests, you can use the example in ``tests/e2e/test_example.py``.
The given test runs against the Wikipedia app.

.. code-block:: console

    $ pytest tests/e2e/test_example.py

.. note::

    Prior to running the above test, you might want to build the `Wikipedia iOS project <https://github.com/wikimedia/wikipedia-ios>`_.
    Simply run: ``make build.wikipedia.ios``.
    The app will be placed under ``tmp/apps/Wikipedia.app``

**Step 5: Format changes**

.. code-block:: console

    $ make format

This step formats the code with autoflake_, isort_, black_, etc.

**Step 6: Run unit tests**

.. code-block:: console

    $ make test.unit # <-- unit tests

**Step 7: Commit changes and create pull requests**


Conventions
-----------
Branch name
~~~~~~~~~~~
If creating branches on the main/original repo (when not using forks), please prefix the branch with your name such as ``chris/my_working_branch``. This way, we know to whom a branch belongs.

Commit message
~~~~~~~~~~~~~~
It is good to reflect the type of the change in the commit message. Let's use this simple convention as follows.

.. code-block:: console

    <CHANGE-TYPE>: <Summary of the change>

As follows are some examples of the commit message:

.. code-block:: console

    FEAT: Detect number of parallel runners
    CHORE: Update default timeout of build jobs
    FIX: Crashed tests are not detected
    REFACTOR: Test retry logic
    DOC: Update Contributing guidelines

Pull request (PR)
~~~~~~~~~~~~~~~~~~
For PR title, let's use the same convention with commit message.
