"""
This module holds unit tests and fixtures for the SuccessfulDockingDoneFunction.

Author: John McCarroll
"""

import numpy as np
import pytest
from act3_rl_core.dones.done_func_base import DoneStatusCodes

from saferl.dones.docking_dones import SuccessfulDockingDoneFunction

test_configs = [
    # (platform_position, platform_velocity, docking_region_radius, velocity_limit, expected_value, expected_status),
    (np.array([9, 0, 0]), np.array([0, 0, 0]), 10, 10, True, DoneStatusCodes.WIN),
    (np.array([10, 0, 0]), np.array([0, 0, 0]), 10, 10, True, DoneStatusCodes.WIN),
    (np.array([11, 0, 0]), np.array([0, 0, 0]), 10, 10, False, None),
    (np.array([9, 0, 0]), np.array([9, 0, 0]), 10, 10, True, DoneStatusCodes.WIN),
    (np.array([9, 0, 0]), np.array([10, 0, 0]), 10, 10, True, DoneStatusCodes.WIN),
    (np.array([9, 0, 0]), np.array([11, 0, 0]), 10, 10, True, DoneStatusCodes.LOSE),
]


@pytest.fixture()
def platform_position(request):
    """
    Parameterized fixture for returning platform position defined in test_configs.

    Returns
    -------
    numpy.ndarray
        Three element array describing platform's 3D position
    """
    return request.param


@pytest.fixture()
def platform_velocity(request):
    """
    Parameterized fixture for returning platform position defined in test_configs.

    Returns
    -------
    numpy.ndarray
        Three element array describing platform's 3D position
    """
    return request.param


@pytest.fixture()
def docking_region_radius(request):
    """
    Parameterized fixture for returning the max_distance passed to the MaxDistanceDoneFunction's constructor, as defined
    in test_configs.

    Returns
    -------
    int
        The max allowed distance in a docking episode
    """
    return request.param


@pytest.fixture()
def velocity_limit(request):
    """
    Parameterized fixture for returning the max_distance passed to the SuccessfulDockingDoneFunction's constructor, as
    defined in test_configs.

    Returns
    -------
    int
        The max allowed distance in a docking episode
    """
    return request.param


@pytest.fixture()
def cut(cut_name, agent_name, docking_region_radius, velocity_limit):
    """
    A fixture that instantiates a SuccessfulDockingDoneFunction and returns it.

    Parameters
    ----------
    cut_name : str
        The name of the component under test
    agent_name : str
        The name of the agent
    docking_region_radius : int
        The radius of the docking region passed to the SuccessfulDockingDoneFunction constructor
    velocity_limit : int
        The velocity limit passed to the SuccessfulDockingDoneFunction constructor

    Returns
    -------
    SuccessfulDockingDoneFunction
        An instantiated component under test
    """
    return SuccessfulDockingDoneFunction(
        name=cut_name, agent_name=agent_name, docking_region_radius=docking_region_radius, velocity_limit=velocity_limit
    )


@pytest.mark.unit_test
@pytest.mark.parametrize(
    "platform_position,platform_velocity,docking_region_radius,velocity_limit,expected_value,expected_status", test_configs, indirect=True
)
def test_call(call_results, next_state, agent_name, cut_name, expected_value, expected_status):
    """
    A parameterized test to ensure that the SuccessfulDockingDoneFunction behaves as intended.

    Parameters
    ----------
    call_results : DoneDict
        The resulting DoneDict from calling the SuccessfulDockingDoneFunction
    next_state : StateDict
        The StateDict that may have been mutated by the SuccessfulDockingDoneFunction
    agent_name : str
        The name of the agent
    cut_name : str
        The name of the component under test
    expected_value : bool
        The expected bool corresponding to whether the agent's episode is done or not
    expected_status : None or DoneStatusCodes
        The expected status corresponding to the status of the agent's episode
    """
    assert call_results[agent_name] == expected_value
    assert next_state.episode_state[agent_name][cut_name] is expected_status
