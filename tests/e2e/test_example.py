from e2e.tester import Tester


def test_example(tester: Tester):
    tester.ui.login.login()
    tester.ui.home.element('Skip').must_exist()
    tester.ui.home.button('Next').tap()
    tester.ui.home.button('Next').tap()
    tester.ui.home.button('Next').tap()
    tester.ui.base.wait()
    tester.ui.home.go_to_settings()
