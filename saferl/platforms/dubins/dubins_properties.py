"""
--------------------------------------------------------------------------
Air Force Research Laboratory (AFRL) Autonomous Capabilities Team (ACT3)
Reinforcement Learning (RL) Core  Extension.

This is a US Government Work not subject to copyright protection in the US.

The use, dissemination or disclosure of data in this file is subject to
limitation or restriction. See accompanying README and LICENSE for details.
---------------------------------------------------------------------------

This module defines the measurement and control properties for Dubins aircraft sensors and controllers.
"""

import typing

import numpy as np
from corl.libraries.property import BoxProp
from pydantic import Field, StrictFloat, StrictStr
from typing_extensions import Annotated


class AccelerationProp(BoxProp):
    """
    Acceleration control properties.

    name : str
        Control property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "acceleration"
    low: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [-29.4132]
    high: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [29.4132]
    unit: Annotated[typing.List[StrictStr], Field(min_items=1, max_items=1)] = ["m/s^2"]
    description: str = "Direct Acceleration Control"


class YawRateProp(BoxProp):
    """
    Yaw rate control properties.

    name : str
        Control property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "yaw_rate"
    low: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [np.deg2rad(-10)]
    high: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [np.deg2rad(10)]
    unit: Annotated[typing.List[StrictStr], Field(min_items=1, max_items=1)] = ["rad/s"]
    description: str = "Direct Yaw Rate Control"


class PitchRateProp(BoxProp):
    """
    Pitch rate control properties.

    name : str
        Control property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "pitch_rate"
    low: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [np.deg2rad(-10)]
    high: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [np.deg2rad(10)]
    unit: Annotated[typing.List[StrictStr], Field(min_items=1, max_items=1)] = ["rad/s"]
    description: str = "Direct Pitch Rate Control"


class RollRateProp(BoxProp):
    """
    Roll rate control properties.

    name : str
        Control property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "roll_rate"
    low: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [np.deg2rad(-10)]
    high: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [np.deg2rad(10)]
    unit: Annotated[typing.List[StrictStr], Field(min_items=1, max_items=1)] = ["rad/s"]
    description: str = "Direct Roll Rate Control"


class YawAndAccelerationProp(BoxProp):
    """
    Combined Yaw Rate and Acceleration control properties.

    name : str
        Control property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "yaw_acceleration"
    low: Annotated[typing.List[StrictFloat], Field(min_items=2, max_items=2)] = [np.deg2rad(-10), -29.4132]
    high: Annotated[typing.List[StrictFloat], Field(min_items=2, max_items=2)] = [np.deg2rad(10), 29.4132]
    unit: Annotated[typing.List[StrictStr], Field(min_items=2, max_items=2)] = ["rad/s", "m/s^2"]
    description: str = "Direct Yaw Rate and Acceleration Control"


class PitchRollAndAccelerationProp(BoxProp):
    """
    Combined Pitch Rate, Roll Rate, and Acceleration control properties.

    name : str
        Control property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "pitch_roll_acceleration"
    low: Annotated[typing.List[StrictFloat], Field(min_items=3, max_items=3)] = [np.deg2rad(-5), np.deg2rad(-10), -29.4132]
    high: Annotated[typing.List[StrictFloat], Field(min_items=3, max_items=3)] = [np.deg2rad(5), np.deg2rad(10), 29.4132]
    unit: Annotated[typing.List[StrictStr], Field(min_items=3, max_items=3)] = ["rad/s", "rad/s", "m/s^2"]
    description: str = "Direct Pitch Rate, Roll Rate and Acceleration Control"


class PositionProp(BoxProp):
    """
    Position sensor properties.

    name : str
        Sensor property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "position"
    low: Annotated[typing.List[StrictFloat], Field(min_items=3, max_items=3)] = [-500000.0] * 3
    high: Annotated[typing.List[StrictFloat], Field(min_items=3, max_items=3)] = [500000.0] * 3
    unit: Annotated[typing.List[StrictStr], Field(min_items=3, max_items=3)] = ["m"] * 3
    description: str = "Position Sensor Properties"


class VelocityProp(BoxProp):
    """
    Velocity sensor properties.

    name : str
        Sensor property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "velocity"
    low: Annotated[typing.List[StrictFloat], Field(min_items=3, max_items=3)] = [-609.6] * 3
    high: Annotated[typing.List[StrictFloat], Field(min_items=3, max_items=3)] = [609.6] * 3
    unit: Annotated[typing.List[StrictStr], Field(min_items=3, max_items=3)] = ["m/s"] * 3
    description: str = "Velocity Sensor Properties"


class HeadingProp(BoxProp):
    """
    Heading sensor properties.

    name : str
        Sensor property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "heading"
    low: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [-np.pi]
    high: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [np.pi]
    unit: Annotated[typing.List[StrictStr], Field(min_items=1, max_items=1)] = ["rad"]
    description: str = "Heading Sensor Properties"


class FlightPathProp(BoxProp):
    """
    Flight path sensor properties.

    name : str
        Sensor property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "flight_path"
    low: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [-np.pi]
    high: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [np.pi]
    unit: Annotated[typing.List[StrictStr], Field(min_items=1, max_items=1)] = ["rad"]
    description: str = "Flight Path Sensor Properties"


class RollProp(BoxProp):
    """
    Roll sensor properties.

    name : str
        Sensor property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "roll"
    low: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [-np.pi]
    high: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [np.pi]
    unit: Annotated[typing.List[StrictStr], Field(min_items=1, max_items=1)] = ["rad"]
    description: str = "Roll Sensor Properties"


class QuaternionProp(BoxProp):
    """
    Quaternion sensor properties.

    name : str
        Sensor property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "quaternion"
    low: Annotated[typing.List[StrictFloat], Field(min_items=4, max_items=4)] = [-1.] * 4
    high: Annotated[typing.List[StrictFloat], Field(min_items=4, max_items=4)] = [1.] * 4
    unit: Annotated[typing.List[StrictStr], Field(min_items=4, max_items=4)] = ["None"] * 4
    description: str = "Quaternion Sensor Properties"


class SpeedProp(BoxProp):
    """
    Speed sensor properties.

    name : str
        Sensor property name.
    low : list[float]
        Minimum bounds of sensor output.
    high : list[float]
        Maximum bounds of sensor output.
    unit : str
        Unit of measurement for sensor output.
    description : str
        Description of sensor properties.
    """

    name: str = "speed"
    low: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [60.96]
    high: Annotated[typing.List[StrictFloat], Field(min_items=1, max_items=1)] = [121.92]
    unit: Annotated[typing.List[StrictStr], Field(min_items=1, max_items=1)] = ["m/s"]
    description: str = "Speed Sensor Properties"