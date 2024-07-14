import types
from typing import TYPE_CHECKING

from e2e._typing import WD
from e2e.core.simulation import Simulation
from e2e.mixin.dynamic import DynamicAttrsMixin

from .location_update import LocationUpdateSimulation
from .push_notification import PushNotificationSimulation

if TYPE_CHECKING:
    from e2e_ext._typing import SimulationsTyping
else:
    SimulationsTyping = types.new_class('Empty')


class Simulations(SimulationsTyping, DynamicAttrsMixin):
    location_update: LocationUpdateSimulation
    push_notification: PushNotificationSimulation

    def __init__(self, wd: WD, source_dir='e2e_ext/simulations') -> None:
        self.wd = wd
        self.base = Simulation(wd=wd)
        self.set_dynamic_attrs(
            cls=Simulation,
            attr_kwargs={'wd': self.wd},
            load_source_in_dir=source_dir,
        )
