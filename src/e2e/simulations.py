import types
from typing import TYPE_CHECKING

from e2e.core.simulation import Simulation
from e2e.mixin.dynamic import DynamicAttrsMixin

if TYPE_CHECKING:
    from e2e_ext._typing import SimulationsTyping
else:
    SimulationsTyping = types.new_class('Empty')


class Simulations(SimulationsTyping, DynamicAttrsMixin):
    def __init__(self) -> None:
        self.base = Simulation()
        self.set_dynamic_attrs(
            cls=Simulation,
            load_source_in_dir='e2e_ext/simulations',
        )
