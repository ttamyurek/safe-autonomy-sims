"""
--------------------------------------------------------------------------
Air Force Research Laboratory (AFRL) Autonomous Capabilities Team (ACT3)
Reinforcement Learning (RL) Core  Extension.

This is a US Government Work not subject to copyright protection in the US.

The use, dissemination or disclosure of data in this file is subject to
limitation or restriction. See accompanying README and LICENSE for details.
---------------------------------------------------------------------------

Functions that define the terminal conditions for the Inspection Environment.
This in turn defines whether the end of an episode has been reached.
"""
import typing
from collections import OrderedDict

import numpy as np
from corl.dones.done_func_base import DoneFuncBase, DoneFuncBaseValidator, DoneStatusCodes, SharedDoneFuncBase, SharedDoneFuncBaseValidator
from corl.libraries.environment_dict import DoneDict
from corl.libraries.state_dict import StateDict

from safe_autonomy_sims.utils import get_closest_fft_distance


class SuccessfulInspectionDoneValidator(DoneFuncBaseValidator):
    """
    This class validates that the config contains the Inspection_region_radius data needed for
    computations in the SuccessfulInspectionDoneFunction.

    inspection_entity_name: str
        The name of the entity under inspection.
    weight_threshold : float
        Points score value indicating success.
        By default None, so success occurs when all points are inspected
    """
    inspection_entity_name: str = "chief"
    weight_threshold: typing.Union[float, None] = None


class SuccessfulInspectionDoneFunction(DoneFuncBase):
    """
    A done function that determines if the deputy has successfully inspected the chief.

    def __call__(self, observation, action, next_observation, next_state):

    Parameters
    ----------
    observation : OrderedDict
        the current observation
    action : OrderedDict
        the current action
    next_observation : OrderedDict
        the incoming observation
    next_state : StateDict
        the incoming state
    observation_space: StateDict
        the observation space
    observation_units: StateDict
        the observation units

    Returns
    -------
    done : DoneDict
        Dictionary containing the done condition for the current agent.
    """

    def __init__(self, **kwargs) -> None:
        self.config: SuccessfulInspectionDoneValidator
        super().__init__(**kwargs)

    @property
    def get_validator(self):
        """
        Parameters
        ----------
        cls : constructor function

        Returns
        -------
        SuccessfulInspectionDoneValidator
            Config validator for the SuccessfulInspectionDoneFunction.
        """
        return SuccessfulInspectionDoneValidator

    def __call__(
        self,
        observation: OrderedDict,
        action: OrderedDict,
        next_observation: OrderedDict,
        next_state: StateDict,
        observation_space: StateDict,
        observation_units: StateDict,
    ) -> DoneDict:
        done = DoneDict()

        if self.config.weight_threshold is not None:
            weight = next_state.inspection_points_map[self.config.inspection_entity_name].get_total_weight_inspected()
            done_check = weight >= self.config.weight_threshold
        else:
            inspection_points = next_state.inspection_points_map[self.config.inspection_entity_name]
            done_check = all(inspection_points.points_inspected_dict.values())

        done[self.config.platform_name] = done_check
        if done[self.config.platform_name]:
            next_state.episode_state[self.config.platform_name][self.name] = DoneStatusCodes.WIN
        self._set_all_done(done)
        return done


class SafeSuccessfulInspectionDoneValidator(SuccessfulInspectionDoneValidator):
    """
    mean_motion : float
        orbital mean motion in rad/s of current Hill's reference frame
    crash_region_radius : float
        The radius of the crashing region in meters.
    fft_time_step : float
        Time step to compute the FFT trajectory. FFT is computed for 1 orbit.
    """
    mean_motion: float
    crash_region_radius: float
    fft_time_step: float = 1


class SafeSuccessfulInspectionDoneFunction(SuccessfulInspectionDoneFunction):
    """
    A done function that determines if the deputy has successfully inspected the chief.
    Considers if a Free Flight Trajectory once the episode ends would result in a collision.
    """

    def __init__(self, **kwargs) -> None:
        self.config: SafeSuccessfulInspectionDoneValidator
        super().__init__(**kwargs)

    @property
    def get_validator(self):
        """
        Config validator for the SafeSuccessfulInspectionDoneFunction.
        """
        return SafeSuccessfulInspectionDoneValidator

    def __call__(
        self,
        observation: OrderedDict,
        action: OrderedDict,
        next_observation: OrderedDict,
        next_state: StateDict,
        observation_space: StateDict,
        observation_units: StateDict,
    ) -> DoneDict:

        done = super().__call__(observation, action, next_observation, next_state, observation_space, observation_units)

        if done[self.config.platform_name]:
            pos = observation[self.config.agent_name]['ObserveSensor_Sensor_Position']['direct_observation']
            vel = observation[self.config.agent_name]['ObserveSensor_Sensor_Velocity']['direct_observation']
            state = np.concatenate((pos, vel))
            n = self.config.mean_motion
            times = np.arange(0, 2 * np.pi / n, self.config.fft_time_step)
            dist = get_closest_fft_distance(state, self.config.mean_motion, times)
            if dist >= self.config.crash_region_radius:
                next_state.episode_state[self.config.platform_name][self.name] = DoneStatusCodes.WIN
            else:
                done[self.config.platform_name] = False
                self._set_all_done(done)

        return done


class CrashAfterSuccessfulInspectionDoneFunction(SuccessfulInspectionDoneFunction):
    """
    A done function that determines if the deputy has successfully inspected the chief.
    Considers if a Free Flight Trajectory once the episode ends would result in a collision.
    """

    def __init__(self, **kwargs) -> None:
        self.config: SafeSuccessfulInspectionDoneValidator
        super().__init__(**kwargs)

    @property
    def get_validator(self):
        """
        Config validator for the SafeSuccessfulInspectionDoneFunction.
        """
        return SafeSuccessfulInspectionDoneValidator

    def __call__(
        self,
        observation: OrderedDict,
        action: OrderedDict,
        next_observation: OrderedDict,
        next_state: StateDict,
        observation_space: StateDict,
        observation_units: StateDict,
    ) -> DoneDict:

        done = super().__call__(observation, action, next_observation, next_state, observation_space, observation_units)

        if done[self.config.platform_name]:
            pos = observation[self.config.agent_name]['ObserveSensor_Sensor_Position']['direct_observation']
            vel = observation[self.config.agent_name]['ObserveSensor_Sensor_Velocity']['direct_observation']
            state = np.concatenate((pos, vel))
            n = self.config.mean_motion
            times = np.arange(0, 2 * np.pi / n, self.config.fft_time_step)
            dist = get_closest_fft_distance(state, self.config.mean_motion, times)
            if dist < self.config.crash_region_radius:
                next_state.episode_state[self.config.platform_name][self.name] = DoneStatusCodes.LOSE
            else:
                done[self.config.platform_name] = False
                self._set_all_done(done)

        return done


class MultiagentSuccessfulInspectionDoneFunctionValidator(SharedDoneFuncBaseValidator):
    """
    The validator for the MultiagentSuccessfulDockingDoneFunction.

    inspection_entity_name: str
        The name of the entity under inspection.
    weight_threshold : float
        Points score value indicating success.
        By default None, so success occurs when all points are inspected
    """
    inspection_entity_name: str = "chief"
    weight_threshold: typing.Union[float, None] = None


class MultiagentSuccessfulInspectionDoneFunction(SharedDoneFuncBase):
    """
    This done function determines whether every agent in the environment
    has reached a specified successful done condition.

    def __call__(self, observation, action, next_observation, next_state, local_dones, local_done_info):

    Parameters
    ----------
    observation : OrderedDict
        the current observation
    action : OrderedDict
        the current action
    next_observation : OrderedDict
        the incoming observation
    next_state : StateDict
        the incoming state
    observation_space: StateDict
        the observation space
    observation_units: StateDict
        the observation units
    local_dones: DoneDict
        DoneDict containing name to boolean KVPs representing done statuses of each agent
    local_done_info: OrderedDict
        An OrderedDict containing nested OrderedDicts of done function to done status KVPs for each agent

    Returns
    -------
    done : DoneDict
        Dictionary containing the done condition for each agent.
    """

    @property
    def get_validator(self) -> typing.Type[SharedDoneFuncBaseValidator]:
        """
        Returns the validator for this done function.

        Returns
        -------
        MultiagentSuccessfulDockingDoneFunctionValidator
            done function validator
        """
        return MultiagentSuccessfulInspectionDoneFunctionValidator

    def __call__(
        self,
        observation: OrderedDict,
        action: OrderedDict,
        next_observation: OrderedDict,
        next_state: StateDict,
        observation_space: StateDict,
        observation_units: StateDict,
        local_dones: DoneDict,
        local_done_info: OrderedDict
    ) -> DoneDict:

        done = DoneDict()

        if self.config.weight_threshold is not None:
            weight = next_state.inspection_points_map[self.config.inspection_entity_name].get_total_weight_inspected()
            done_check = weight >= self.config.weight_threshold
        else:
            inspection_points = next_state.inspection_points_map[self.config.inspection_entity_name]
            done_check = all(inspection_points.points_inspected_dict.values())

        if done_check:
            for k in local_dones.keys():
                done[k] = True

        return done
