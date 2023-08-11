from e2e._typing import WD
from e2e.screens import Screens
from e2e.simulations import Simulations


class Tester:
    __test__ = False

    def __init__(self, wd: WD) -> None:
        self.wd = wd
        self.ui = Screens(wd=wd)
        self.simulations = Simulations()
