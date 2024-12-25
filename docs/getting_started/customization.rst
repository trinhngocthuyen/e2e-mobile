Customizing ``Screen``, ``Simulation``, and ``Tester``
======================================================

The e2e-mobile package provides a number of useful features to interact with the app.
You can also add your customizations to the base classes.

When initializing the project with ``e2e init``, the package creates the custom classes: ``Screen``, ``Simulation``, and ``Tester`` under ``e2e_ext/core`` directory. These are where you can put your customizations, for example - adding a method ``shake_phone`` to ``Tester``.

.. code-block::

  e2e_ext / --- core / --- screen.py
                      |--- simulation.py
                      |--- tester.py
