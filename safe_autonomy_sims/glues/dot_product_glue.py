"""
--------------------------------------------------------------------------
Air Force Research Laboratory (AFRL) Autonomous Capabilities Team (ACT3)
Reinforcement Learning (RL) Core  Extension.

This is a US Government Work not subject to copyright protection in the US.

The use, dissemination or disclosure of data in this file is subject to
limitation or restriction. See accompanying README and LICENSE for details.
---------------------------------------------------------------------------

Glue which returns the dot product between the deputy orientation unit
vector and the unit vector pointing from the deputy to the chief.

Author: Kochise Bennett
"""
import typing
from collections import OrderedDict

import gym
import numpy as np
from corl.glues.base_multi_wrapper import BaseMultiWrapperGlue, BaseMultiWrapperGlueValidator


class DotProductGlueValidator(BaseMultiWrapperGlueValidator):
    """
    Validator for the DotProductGlue.

    position_obs_name: str
        Name of the observation space entry corresponding to the position of the
        deputy in Hill's frame.
    orientation_obs_name: str
        Name of the observation space entry corresponding to the unit vector 
        pointing in the direction of the deputy's orientation in Hill's frame.
    """
    normalize_obs_vectors : bool  = False

class DotProductGlue(BaseMultiWrapperGlue):
    """
    Computes dot product between the deputy orientation unit vector and the 
    unit vector pointing from the deputy to the chief
    """
    
    class Fields:
        """
        Fields in this glue
        """
        DIRECT_OBSERVATION = "direct_observation"

    @property
    def get_validator(self) -> typing.Type[DotProductGlueValidator]:
        return DotProductGlueValidator

    def get_unique_name(self) -> str:
        glue_name0 = self.glues()[0].get_unique_name()
        glue_name1 = self.glues()[1].get_unique_name()
        return glue_name0 + "_DotProduct_" + glue_name1
    
    def observation_units(self):
        d = gym.spaces.dict.Dict()
        d.spaces[self.Fields.DIRECT_OBSERVATION] = ['N/A']
        return d

    def observation_space(self):
        d = gym.spaces.dict.Dict()
        d.spaces[self.Fields.DIRECT_OBSERVATION] = gym.spaces.Box(-1.0, 1.0, shape=(1,), dtype=np.float32)
        return d

    def get_observation(self, other_obs: OrderedDict, obs_space: OrderedDict, obs_units: OrderedDict):
        glue0 = self.glues()[0]
        glue1 = self.glues()[1]

        obs0 = glue0.get_observation(other_obs, obs_space, obs_units)[glue0.Fields.DIRECT_OBSERVATION]
        obs1 = glue1.get_observation(other_obs, obs_space, obs_units)[glue1.Fields.DIRECT_OBSERVATION]

        dot_product = np.dot(obs0, obs1)

        if self.config.normalize_obs_vectors:
            dot_product = dot_product / (np.linalg.norm(obs0) * np.linalg.norm(obs1) + 1e-5)
        
        dot_product = np.clip(dot_product, -1.0, 1.0)
        
        d = OrderedDict()
        d[self.Fields.DIRECT_OBSERVATION] = np.array([dot_product], dtype=np.float32)
        return d
