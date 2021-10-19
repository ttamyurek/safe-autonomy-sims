import numpy as np
from act3_rl_core.libraries.property import MultiBoxProp
from act3_rl_core.simulators.base_parts import BaseController, BaseControllerValidator


class DubinsController(BaseController):

    @property
    def name(self):
        return self.config.name + self.__class__.__name__

    def apply_control(self, control: np.ndarray) -> None:
        raise NotImplementedError

    def get_applied_control(self) -> np.ndarray:
        raise NotImplementedError


class DubinsPassThroughController(DubinsController):
    def __init__(
        self,
        parent_platform,  # type: ignore # noqa: F821
        config,
    ):
        control_props = MultiBoxProp(
            name="Dubins Control Vector", low=[-10], high=[10], unit=["m/s"], description="Velocity")
        super().__init__(control_properties=control_props, parent_platform=parent_platform, config=config)
        self.control_properties.name = self.config.name

    def apply_control(self, control: np.ndarray) -> None:
        self._parent_platform.next_action[THROTTLE_CONTROL] = control

    def get_applied_control(self) -> np.ndarray:
        return np.array([self._parent_platform.next_action[THROTTLE_CONTROL]], dtype=np.float32)


class ThrottleController(DubinsController):

    def __init__(
        self,
        parent_platform,  # type: ignore # noqa: F821
        config,
    ):
        control_props = MultiBoxProp(name="", low=[-10], high=[10], unit=["m/s"], description="Velocity")
        super().__init__(control_properties=control_props, parent_platform=parent_platform, config=config)
        self.control_properties.name = self.config.name

    def apply_control(self, control: np.ndarray) -> None:
        self._parent_platform.next_action[THROTTLE_CONTROL] = control

    def get_applied_control(self) -> np.ndarray:
        return np.array([self._parent_platform.next_action[THROTTLE_CONTROL]], dtype=np.float32)
