from e2e_ext.screens.example import ExampleScreen
from e2e_ext.screens.home import HomeScreen
from e2e_ext.screens.settings import SettingsScreen
from e2e_ext.simulations.example import ExampleSimulation


class ScreensTyping:
    settings: SettingsScreen
    example: ExampleScreen
    home: HomeScreen


class SimulationsTyping:
    example: ExampleSimulation
