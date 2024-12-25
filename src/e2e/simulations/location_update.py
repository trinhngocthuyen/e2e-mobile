from cicd.core.utils.sh import sh

from e2e.core.env import Platform, env
from e2e.core.simulation import Simulation
from e2e.core.utils import WDUtils


class LocationUpdateSimulation(Simulation):
    DEFAULT_LAT = 1.2837575  # Marina Bay Sands (Singapore)
    DEFAULT_LNG = 103.8565316  # Marina Bay Sands (Singapore)

    def run(self, **kwargs):
        if (lat := kwargs.get('lat')) is None:
            lat = self.DEFAULT_LAT
        if (lng := kwargs.get('lng')) is None:
            lng = self.DEFAULT_LNG

        if env.platform == Platform.IOS:
            self.ios_update_location(lat=lat, lng=lng)
        else:
            self.logger.warning(f'Location update is not yet implemented for platform: {env.platform}')

    def ios_update_location(self, lat: float, lng: float):
        device = WDUtils.device_from_caps(self.wd.capabilities)
        self.logger.debug(f'Update location: {lat = }, {lng = }')
        sh.exec(f'xcrun simctl location {device} set {lat},{lng}')

    def __call__(self, lat: float | None = None, lng: float | None = None) -> 'LocationUpdateSimulation':
        return super().__call__(lat=lat, lng=lng)
