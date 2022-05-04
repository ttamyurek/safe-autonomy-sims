"""
Contains implementations of sensors that can be used in injuction with the CWH platform
"""

from corl.libraries.plugin_library import PluginLibrary
from corl.simulators.base_parts import BaseSensor

import saferl.core.platforms.cwh.cwh_properties as cwh_props
from saferl.core.platforms.cwh.cwh_available_platforms import CWHAvailablePlatformTypes
from saferl.core.simulators.cwh_simulator import CWHSimulator


class CWHSensor(BaseSensor):
    """
    Interface for a basic sensor of the CWH platform
    """

    def _calculate_measurement(self, state):
        """
        get measurements from the sensor

        Raises
        ------
        NotImplementedError
            If the method has not been implemented
        """
        raise NotImplementedError


PluginLibrary.AddClassToGroup(CWHSensor, "Sensor_Generic", {"simulator": CWHSimulator, "platform_type": CWHAvailablePlatformTypes.CWH})


class PositionSensor(CWHSensor):
    """
    Implementation of a sensor designed to give the position at any time
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.PositionProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - position

        Returns
        -------
        list of floats
            position of spacecraft
        """
        return self.parent_platform.position


PluginLibrary.AddClassToGroup(
    PositionSensor, "Sensor_Position", {
        "simulator": CWHSimulator, "platform_type": CWHAvailablePlatformTypes.CWH
    }
)


class VelocitySensor(CWHSensor):
    """
    Implementation of a sensor to give velocity at any time
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.VelocityProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    # state - tuple
    def _calculate_measurement(self, state):
        """
        Calculate the measurement - velocity

        Returns
        -------
        list of floats
            velocity of spacecraft
        """
        return self.parent_platform.velocity


PluginLibrary.AddClassToGroup(
    VelocitySensor, "Sensor_Velocity", {
        "simulator": CWHSimulator, "platform_type": CWHAvailablePlatformTypes.CWH
    }
)