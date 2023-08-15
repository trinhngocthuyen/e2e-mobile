from e2e import Tester


def test_example(tester: Tester):
    # Check if tutorial shows up, but only once
    tester.ui.home.skip_tutorial()
    tester.take_screenshot()
    tester.relaunch_app()
    tester.ui.home.must_not_see_tutorial()

    # Trigger a simulation
    with tester.simulations.example:
        pass

    # Check elements in settings
    tester.ui.home.go_to_settings()
    tester.ui.settings.swipe('up')
    tester.ui.settings.element('About the app').must_exist()
    tester.ui.settings.swipe('down')
    tester.ui.settings.close()

    # Check search screen
    tester.ui.home.button('Search').tap()
    tester.ui.home.textfield('Search Wikipedia').input('Facebook')
    tester.ui.home.element('Social networking service').tap()
    tester.ui.home.button('Back').tap()
