from e2e._typing import WD
from e2e.core.mixin.ui import UIMixin


class Screen(UIMixin):
    '''Base class for UI assertions and actions.
    For example, inputting username and password in the login screen, then tapping the login button.
    A Screen class corresponds to a screen in the app. This helps make test suites more readable.

    Following is the example of actions in the login screen:

    .. code-block:: python

        class LoginScreen(Screen):
            def login(self):
                self.textfield('Username').input('foo')
                self.textfield('Password').input('bar')
                self.button('Login').tap()
    '''

    def __init__(self, wd: WD) -> None:
        self.wd = wd
