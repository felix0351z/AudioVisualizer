import numpy as np
from typing import Optional

import input
import sender

from src.effects.effect import AudioEffect, EffectDescription
from src.effects.melbank import MelbankEffect
from src.effects.spectrum import SpectrumEffect


class SingleProgram:
    EFFECTS: list[AudioEffect] = [
        MelbankEffect(), SpectrumEffect()
    ]

    # sender, effekte, farben, (view, input)

    def __init__(self, callback):
        self.current_effect: Optional[AudioEffect] = None
        self.callback = callback

        self.worker = input.BufferThread(self.process)
        self.sender = sender.SacnSender()

    def __del__(self):
        pass

    def get_effects(self) -> [EffectDescription]:
        descriptions = []
        for effect in self.EFFECTS:
            descriptions.append(effect.description())

        return descriptions

    def get_selected_effect(self) -> EffectDescription:
        return self.current_effect.description()

    def set_effect(self, position: int):
        try:
            self.current_effect = self.EFFECTS[position]
        except IndexError:
            print(f"Effect at index {position} not found!")

        self.current_effect.start()

    def start(self):
        self.worker.start()
        pass

    def pause(self):
        pass

    def process(self, raw: np.ndarray):
        signal = self.current_effect.visualize(raw)
        self.sender.send_signal(signal)
        self.callback(signal)
