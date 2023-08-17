Examples
========

Some examples are available under ``tests/e2e`` of this repo:
https://github.com/trinhngocthuyen/e2e-mobile/tree/main/tests/e2e

Take a look at `test_settings.py <https://github.com/trinhngocthuyen/e2e-mobile/tree/main/tests/e2e/test_settings.py>`_, for example. There are several tests to verify features under this Settings screen.

Running a particular test inside a test file
--------------------------------------------

To run a particular test with pytest:

.. code-block:: console

    $ pytest <path/to/file>::<test_method>

For instance, to run the test ``test_forgot_password`` inside this file:

.. code-block:: console

    $ pytest tests/e2e/test_settings.py::test_forgot_password

Leveraging fixtures for reusable test setup
-------------------------------------------

As you can see, in this file, we create some fixtures such as ``take_me_to_settings`` and ``take_me_to_login``.

.. code-block:: python

    @pytest.fixture
    def take_me_to_settings(tester: Tester):
        tester.ui.home.skip_tutorial()
        tester.ui.home.go_to_settings()


    @pytest.fixture
    def take_me_to_login(tester: Tester, take_me_to_settings):
        tester.ui.settings.button('Log in').tap()
        tester.ui.element('Log in to your account').must_exist()
        tester.ui.element('Username').must_exist()
        tester.ui.element('Password').must_exist()

These fixtures are incredibly useful. They can be used as a shortcut to performing necessary actions to enter a specific screen.
All you need to do is to add the fixture to the test method signature. Then, the code inside those fixtures will be automatically executed. How convenient! Right 😄?

.. code-block:: python

    def test_login_error(tester: Tester, take_me_to_login): # <-- add the fixture here
        ...

Using xpath when accessibility labels/ids are missing
-----------------------------------------------------

When inspecting the elements, you should see xml of the username textfield like this:

.. code-block:: xml

    <XCUIElementTypeTextField type="XCUIElementTypeTextField" value="enter username" label="" enabled="true" visible="true" accessible="true" x="51" y="233" width="288" height="29" index="4">

As you notice, the ``label=""`` demonstrates that the accessibility label is missing. However, we can use xpath queries to overcome this issue.

At first sight, we can query the element of type ``XCUIElementTypeTextField`` having value as *"enter username"*:

.. code-block:: python

    tester.ui.textfield(xpath='//XCUIElementTypeTextField[@value="enter username"]').input('foo')

This xpath works like a charm. Yet, it's still iOS-specific because of the type ``XCUIElementTypeTextField``. To make it more universal for both platforms, we can update the query to accept any type.

.. code-block:: python

    tester.ui.textfield(xpath='//*[@value="enter username"]').input('foo')

--

Many argue that using xpath is slow. And using xpath queries accepting any type like above is even slower. However, in the context of end-to-end testing, does it matter that much if the queries run 0.5s slower, or even 1-2s slower. Sometimes, it's a compromise between performance and maintenance cost. I'd leave that up to you to decide what's best for your case 😉.
