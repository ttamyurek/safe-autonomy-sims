"""
--------------------------------------------------------------------------
Air Force Research Laboratory (AFRL) Autonomous Capabilities Team (ACT3)
Reinforcement Learning (RL) Core  Extension.

This is a US Government Work not subject to copyright protection in the US.

The use, dissemination or disclosure of data in this file is subject to
limitation or restriction. See accompanying README and LICENSE for details.
---------------------------------------------------------------------------

Contains implementations of sensors that can be used in junction with the CWH platform.
"""
import typing

import numpy as np
from corl.libraries.plugin_library import PluginLibrary
from corl.simulators.base_parts import BasePlatformPartValidator, BaseSensor

import safe_autonomy_sims.platforms.cwh.cwh_properties as cwh_props
from safe_autonomy_sims.platforms.cwh.cwh_available_platforms import CWHAvailablePlatformTypes
from safe_autonomy_sims.simulators.cwh_simulator import CWHSimulator
from safe_autonomy_sims.simulators.inspection_simulator import InspectionSimulator


class CWHSensor(BaseSensor):
    """
    Interface for a basic sensor of the CWH platform.
    """

    def _calculate_measurement(self, state):
        """
        Get measurements from the sensor.

        Raises
        ------
        NotImplementedError
            If the method has not been implemented.
        """
        raise NotImplementedError


class PositionSensor(CWHSensor):
    """
    Implementation of a sensor designed to give the position at any time.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.PositionProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - position.

        Returns
        -------
        list of floats
            Position of spacecraft.
        """
        return self.parent_platform.position


class VelocitySensor(CWHSensor):
    """
    Implementation of a sensor to give velocity at any time.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.VelocityProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    # state - tuple
    def _calculate_measurement(self, state):
        """
        Calculate the measurement - velocity.

        Returns
        -------
        list of floats
            Velocity of spacecraft.
        """
        return self.parent_platform.velocity


class InspectedPointsSensor(CWHSensor):
    """
    Implementation of a sensor to give number of points at any time.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.InspectedPointProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - num_inspected_points.

        Returns
        -------
        int
            Number of inspected points.
        """
        return self.parent_platform.num_inspected_points


class SunAngleSensor(CWHSensor):
    """
    Implementation of a sensor to give the sun angle
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.SunAngleProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - sun angle.

        Returns
        -------
        float
            sun angle
        """
        return self.parent_platform.sun_angle


class UninspectedPointsSensor(CWHSensor):
    """
    Implementation of a sensor to give location of cluster of uninspected points.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.UninspectedPointProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - cluster_location.

        Returns
        -------
        np.ndarray
            Cluster location of the uninspected points.
        """
        return self.parent_platform.cluster_location


class EntitySensorValidator(BasePlatformPartValidator):
    """
    Validator for the EntitySensors
    """
    entity_name: str


class EntityPositionSensor(CWHSensor):
    """
    Implementation of a sensor designed to give the position at any time.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.PositionProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    @property
    def get_validator(self) -> typing.Type[EntitySensorValidator]:
        """
        return the validator that will be used on the configuration
        of this part
        """
        return EntitySensorValidator

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - position.

        Returns
        -------
        list of floats
            Position of spacecraft.
        """
        return state.sim_entities[self.config.entity_name].position


class OriginPositionSensor(CWHSensor):
    """
    Implementation of a sensor designed to give the position at any time.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.PositionProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - position.

        Returns
        -------
        list of floats
            Position of spacecraft.
        """
        return np.array([0, 0, 0])


class BoolArraySensor(CWHSensor):
    """
    Implementation of a sensor to give boolean array for all inspected/uninspected points
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.BoolArrayProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - bool_array.

        Returns
        -------
        np.ndarray
            Bool array describing inspected/uninspected points.
        """
        return self.parent_platform.bool_array


for sim in [CWHSimulator, InspectionSimulator]:
    for platform in [CWHAvailablePlatformTypes.CWH, CWHAvailablePlatformTypes.CWHSixDOF]:
        for sensor, sensor_name in zip(
            [
                CWHSensor,
                PositionSensor,
                VelocitySensor,
                InspectedPointsSensor,
                SunAngleSensor,
                UninspectedPointsSensor,
                EntityPositionSensor,
                OriginPositionSensor,
                BoolArraySensor
            ],
            [
                "Sensor_Generic",
                "Sensor_Position",
                "Sensor_Velocity",
                "Sensor_InspectedPoints",
                "Sensor_SunAngle",
                "Sensor_UninspectedPoints",
                "Sensor_EntityPosition",
                "Sensor_OriginPosition",
                "Sensor_BoolArray"
            ]
        ):
            PluginLibrary.AddClassToGroup(sensor, sensor_name, {"simulator": sim, "platform_type": platform})
