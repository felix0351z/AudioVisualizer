import abc
import numpy as np
from dataclasses import dataclass


@dataclass
class EffectDescription:
    name: str
    description: str
    # config


class AudioEffect:
    NAME = ""
    DESCRIPTION = ""

    @abc.abstractmethod
    def start(self, n_led: int):
        pass

    @abc.abstractmethod
    def visualize(self, raw: np.ndarray) -> np.ndarray:
        pass

    def description(self) -> EffectDescription:
        return EffectDescription(
            self.NAME,
            self.DESCRIPTION
        )
