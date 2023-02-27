from src.dsp.processing import AudioInformation
import numpy as np


class EffectInfo:
    name: str
    description: str


class AudioEffect:

    def info(self) -> EffectInfo:
        pass

    def process(self, data: AudioInformation) -> np.ndarray:
        pass
