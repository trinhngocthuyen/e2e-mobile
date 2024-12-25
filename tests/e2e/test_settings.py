import pytest

from e2e_ext.core import Tester


@pytest.fixture
def take_me_to_settings(tester: Tester):
    '''This is a handy fixture used as a shortcut to the settings screen.
    In any tests performing in the screens after settings, we can just add this fixture
    to the test, then the following code will be automatically executed.
    '''
    tester.ui.home.skip_tutorial()
    tester.ui.home.go_to_settings()


@pytest.fixture
def take_me_to_login(tester: Tester, take_me_to_settings):
    '''This is a handy fixture used as a shortcut to the login screen.
    In any tests performing in the screens after login, we can just add this fixture
    to the test, then the following code will be automatically executed.
    '''
    tester.ui.settings.button('Log in').tap()
    tester.ui.element('Log in to your account').must_exist()
    tester.ui.element('Username').must_exist()
    tester.ui.element('Password').must_exist()


def test_login_error(tester: Tester, take_me_to_login):
    tester.ui.textfield(xpath='//*[@value="enter username"]').input('foo')
    tester.ui.textfield(xpath='//*[@value="enter password"]').input('bar')
    tester.ui.hide_keyboard()
    tester.ui.button('Log in').tap()
    tester.ui.element('Incorrect username or password entered.\nPlease try again.').must_exist()
    tester.ui.wait(5)


def test_forgot_password(tester: Tester, take_me_to_login):
    tester.ui.button('Forgot your password?').tap()
    tester.ui.element('Reset password').must_exist()
    tester.ui.element('Username').must_exist()
    tester.ui.element('Email').must_exist()
    tester.ui.textfield(xpath='//*[@value="enter username"]').must_exist()
    tester.ui.textfield(xpath='//*[@value="example@example.org"]').must_exist()
