Using UI Assertions and Actions
===============================

While testing, we interact with the app in two ways:

- *UI actions*: For example, tapping a button, swiping left, inputting data into a textfield, etc.
- *UI assertions*: For example, we expect to see a text with certain value, a toggle being on, etc.

Using the ``tester`` fixture
----------------------------

The ``tester`` fixture provides the helpers needed to peform UI actions and assertions in your tests.

.. code-block:: python

    def test_example(tester: Tester):
        tester.ui.button('Skip').tap()          # <-- UI action
        tester.ui.element('Today').must_exist() # <-- UI assertion
        tester.ui.tap_area('center')

There are various methods under ``tester.ui`` you can use to work with elements.
Those methods are wrappers on top of Appium APIs to provide you convenience and better readability.

The following table demonstrates some common usages.

.. list-table::
    :header-rows: 1

    * - Method
      - Example
      - Remarks
    * - ``element``
      - ``tester.ui.element('foo').must_exist()``
        ``tester.ui.element('bar').must_not_exist()``
      - Return an element.
    * - ``button``
      - ``tester.ui.button('foo').tap()``
      - Return a button.
    * - ``textfield``
      - ``tester.ui.textfield('foo').input('bar')``
      - Return a textfield.
    * - ``check``
      - ``assert tester.ui.check('foo').exists``
      - Return a check.
        Unlike ``element``, the ``check`` method returns a failurable element. This means if the element does not appear on the screen, ``tester.ui.check('foo')`` will not throw an exception.
    * - ``wait``
      - ``tester.ui.wait(2)``
      - Wait for a duration.
    * - ``tap_area``
      - ``tester.ui.tap_area('center')``
      - Tap on the screen, usually for the tap-to-dismiss scenarios.
    * - ``swipe``
      - ``tester.ui.swipe('up')``
      - Swipe the screen, usually for the scrollable content.

Writing a new ``Screen``
------------------------

To make your tests readable and reusable, you are encouraged to structure your UI assertions and actions code into classes. ``Screen`` is used for this case.

``Screen`` is the base class for UI assertions and actions. A ``Screen`` corresponds to a UI screen in the app. For example, the login UI is a screen, a settings UI is also a screen.

.. code-block:: python

    from e2e_ext.core import Screen

    class SettingsScreen(Screen):
        def logout(self):
            self.button('Log out').tap()

Structuring your code this way, your tests would look more intuitive:

.. code-block:: python

    from e2e_ext.core.tester import Tester

    def test_logout(tester: Tester):
        ...
        tester.ui.settings.logout() # 👈

.. note::

    The methods we mentioned in the previous section (ie. ``button``, ``element``, etc.) are also available in a ``Screen``.

Creating a new ``Screen``
~~~~~~~~~~~~~~~~~~~~~~~~~

To create a new screen, you simply need to run:

.. code-block:: console

    $ e2e new screen [name_in_snake_case]

For example, to create a Settings screen, run:

.. code-block:: console

    $ e2e new screen settings

When running the above command, the sample code is generated under ``e2e_ext/screens/settings.py``. Your task is now filling in the code needed in this file.

Another cool thing is that the type hints in ``e2e_ext/_typing.py`` is also automatically updated. This helps facilitate the autocompletion of the code editor.
