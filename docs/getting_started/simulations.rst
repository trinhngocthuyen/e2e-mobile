Using Simulations
=================

Simulations are meant for test arrangement, sometimes called "test setup".
For example, sending an API request to prepare resources, triggering a push notification, or simulating location updates.

Using the ``tester`` fixture
----------------------------

The ``tester`` fixture provides the skeleton to run a simulation in your tests.
To run a simulation, you simply need to use with the context manager syntax.

.. code-block:: python

    def test_example(tester: Tester):
        with tester.simulations.location_update(lat=0.001, lng=0.001): # <-- trigger a simulation
            pass # <-- perform assertions here

There are various available simulations in ``tester.simulations`` that you can use:

- ``location_update``: Triggering location updates.
- ``push_notification``: Pushing a notification to the app.

Writing a new ``Simulation``
----------------------------

Similar to ``Screen``, the purpose of having ``Simulation`` is to make your logic readable and reusable. To write a new simulation, you just need to subclass ``Simulation`` and place it under ``e2e_ext/simulations``.

.. code-block:: python

    from e2e import Simulation

    class PrepareDataSimulation(Simulation):
        def run(self, **kwargs):
            pass # <-- Implement your logic here

Creating a new ``Simulation``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For convenience, we provide the CLI usage for you to quickly create a new simulation from templates.

.. code-block:: console

    $ e2e new simulation [name-in-snake-case]

For example, to create a "prepare data" simulation, run:

.. code-block:: console

    $ e2e new simulation prepare_data

When running the above command, the sample code is generated under ``e2e_ext/simulations/prepare_data.py``. Your task is now filling in the code needed in this file.

Another cool thing is that the type hints in ``e2e_ext/_typing.py`` is also automatically updated. This helps facilitate the autocompletion of the code editor.
