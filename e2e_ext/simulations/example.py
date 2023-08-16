from e2e import Simulation


class ExampleSimulation(Simulation):
    def run(self, *args, **kwargs):
        self.logger.debug(
            'This is just an example simulation. It does nothing at all.\n'
            'Among the 4 steps of a test (arrange, act, assert, cleanup), '
            'simulations are meant for test arrangement.\n'
            'For example: sending an API request to prepare test resources, '
            'or trigger a push notification.'
        )
