from e2e.tester import Tester


def test_example(tester: Tester):
    tester.screens.login.login()
    tester.screens.base.wait()
    tester.screens.home.go_to_settings()
