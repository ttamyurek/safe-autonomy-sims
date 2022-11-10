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

from corl.dones.done_func_base import DoneFuncBase, DoneFuncBaseValidator, DoneStatusCodes, SharedDoneFuncBase, SharedDoneFuncBaseValidator
from corl.libraries.environment_dict import DoneDict
from corl.libraries.state_dict import StateDict


class SuccessfulInspectionDoneValidator(DoneFuncBaseValidator):
    """
    This class validates that the config contains the Inspection_region_radius data needed for
    computations in the SuccessfulInspectionDoneFunction.

    """
    ...


class SuccessfulInspectionDoneFunction(DoneFuncBase):
    """
    A done function that determines if the deputy has successfully docked with the chief.

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

        all_inspected = True
        for _, inspected in next_state.points.items():
            if not inspected:
                all_inspected = False
                break

        done[self.agent] = bool(all_inspected)
        if done[self.agent]:
            next_state.episode_state[self.agent][self.name] = DoneStatusCodes.WIN
        self._set_all_done(done)
        return done


class MultiagentSuccessfulInspectionDoneFunctionValidator(SharedDoneFuncBaseValidator):
    """
    The validator for the MultiagentSuccessfulDockingDoneFunction.
    """
    ...


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

        all_inspected = False not in next_state.points.values()

        if all_inspected:
            for k in local_dones.keys():
                done[k] = True

        return done