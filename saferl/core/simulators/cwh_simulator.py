"""
This module contains the CWH Simulator for interacting with the CWH Docking task simulator
"""

from corl.libraries.plugin_library import PluginLibrary

from saferl.backend.cwh.cwh import CWHSpacecraft
from saferl.core.platforms.cwh.cwh_platform import CWHPlatform
from saferl.core.simulators.saferl_simulator import SafeRLSimulator


class CWHSimulator(SafeRLSimulator):
    """
    Simulator for CWH Docking Task. Interfaces CWH platforms with underlying CWH entities in Docking simulation.
    """

    def _construct_platform_map(self) -> dict:
        return {
            'default': (CWHSpacecraft, CWHPlatform),
            'cwh': (CWHSpacecraft, CWHPlatform),
        }


PluginLibrary.AddClassToGroup(CWHSimulator, "CWHSimulator", {})