"""
--------------------------------------------------------------------------
Air Force Research Laboratory (AFRL) Autonomous Capabilities Team (ACT3)
Reinforcement Learning (RL) Core  Extension.

This is a US Government Work not subject to copyright protection in the US.

The use, dissemination or disclosure of data in this file is subject to
limitation or restriction. See accompanying README and LICENSE for details.
---------------------------------------------------------------------------

Contains implementations of sensors that can be used in junction with the six dof CWH platform.
"""
from scipy.spatial.transform import Rotation as R
import numpy as np
from corl.libraries.plugin_library import PluginLibrary

import safe_autonomy_sims.platforms.cwh.cwh_properties as cwh_props
from safe_autonomy_sims.platforms.cwh.cwh_available_platforms import CWHAvailablePlatformTypes
from safe_autonomy_sims.platforms.cwh.cwh_sensors import CWHSensor
from safe_autonomy_sims.simulators.cwh_simulator import CWHSimulator
from safe_autonomy_sims.simulators.inspection_simulator import InspectionSimulator


class QuaternionSensor(CWHSensor):
    """
    Implementation of a sensor designed to give the quaternion at any time.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.QuaternionProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - quaternion.

        Returns
        -------
        list of floats
            quaternion of spacecraft.
        """
        return self.parent_platform.quaternion


class AngularVelocitySensor(CWHSensor):
    """
    Implementation of a sensor designed to give the angular velocity at any time.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.AngularVelocityProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - angular_velocity.

        Returns
        -------
        list of floats
            Angular velocity of spacecraft.
        """
        return self.parent_platform.angular_velocity


class OrientationUnitVectorSensor(CWHSensor):
    """
    Implementation of a sensor designed to give the canonical (or reference) 
    sensor orientation unit vector.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.OrientationVectorProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - unit vector.

        Returns
        -------
        list of floats
            elements of unit vector that points in direction of spacecraft 
            sensor.
        """
        quaternion = self.parent_platform.quaternion
        r = R.from_quat(quaternion)
        try:
            initial_orientation = state.inspection_points_map['chief'].config.initial_sensor_unit_vec
        except KeyError:
            return np.array([0.0, 0.0, 0.0])
        if initial_orientation is None:
            return np.array([0.0, 0.0, 0.0])
        # current_orientation = r.apply(initial_orientation)
        return initial_orientation


class RotatedAxesSensor(CWHSensor):
    """
    Implementation of a sensor designed to give the vectors that result from 
    rotating the initial coordinate frame's unit vectors into the deputy's 
    frame.  
    
    Note: Because the canonical initial_sensor_unit_ec is [1, 0, 0] (we assume
    this hasn't been changed), we omit this unit vector.  Thus, the sensor
    returns 6 values, the x,y,x components of the remaining two unit vectors
    after rotation.
    """

    def __init__(self, parent_platform, config, property_class=cwh_props.RotatedAxesProp):
        super().__init__(property_class=property_class, parent_platform=parent_platform, config=config)

    def _calculate_measurement(self, state):
        """
        Calculate the measurement - unit vector.

        Returns
        -------
        list of floats
            elements of unit vector that points in direction of spacecraft 
            sensor.
        """
        quaternion = self.parent_platform.quaternion
        r = R.from_quat(quaternion)
        v1 = np.array([0.0, 1.0, 0.0])
        v2 = np.array([0.0, 0.0, 1.0])
        
        rot_v1 = r.apply(v1)
        rot_v2 = r.apply(v2)
        
        out = np.concatenate([rot_v1, rot_v2])
        return out


for sim in [CWHSimulator, InspectionSimulator]:
    for sensor, sensor_name in zip([QuaternionSensor, AngularVelocitySensor, OrientationUnitVectorSensor, RotatedAxesSensor],
                                   ["Sensor_Quaternion", "Sensor_AngularVelocity", "Sensor_OrientationUnitVector", "Sensor_RotatedAxes"]):
        PluginLibrary.AddClassToGroup(sensor, sensor_name, {"simulator": sim, "platform_type": CWHAvailablePlatformTypes.CWHSixDOF})
