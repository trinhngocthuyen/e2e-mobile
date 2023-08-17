Frequently Asked Questions
==========================

.. contents::
   :local:

Python setup
------------

Why does I get the "command not found: e2e" error?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using the system python, sometimes the package is not recognized. This happens not only to this package but also to others as well. My recommendation is to install python with Homebrew for development.

.. code-block:: console

    $ brew install python@3.10

Note that after installing python with brew, there is a message asking you to export the PATH to the profile. For example, adding the following line to ``~/.zprofile`` to make sure the python version (installed by brew) will be chosen. Remember to restart Terminal after that.

.. code-block:: console

    export PATH="/opt/homebrew/opt/python@3.10/libexec/bin:${PATH}"

To verify, just run ``which python`` to see the actual path. It should be something like ``/opt/homebrew/opt/python@3.10/libexec/bin/python``.
