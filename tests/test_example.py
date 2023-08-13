from e2e.tester import Tester


def test_example(tester: Tester):
    tester.ui.home.complete_tutorial()
    tester.take_screenshot()
    tester.relaunch_app()
    tester.ui.home.button('Search').tap()
    tester.ui.home.textfield('Search Wikipedia').input('Facebook')
    tester.ui.home.element('Social networking service').must_exist()
