import numpy as np
from typing import Optional

import input
import sender

from src.effects.effect import AudioEffect, EffectInformation
from src.effects.melbank import MelbankEffect
from src.effects.spectrum import SpectrumEffect

from src.colors.effect import ColorEffect
from src.colors.single import SingleColor


class SingleProgram:
    EFFECTS: list[AudioEffect] = [
        SpectrumEffect(), MelbankEffect()
    ]

    COLORS: list[ColorEffect] = [
        SingleColor()
    ]

    # sender, effekte, farben, (view, input)

    def __init__(self, callback):
        self.current_color: Optional[ColorEffect] = None
        self.current_effect: Optional[AudioEffect] = None
        self.callback = callback

        self.worker = input.BufferThread(self.process)  # Create a worker thread
        self.sender = sender.SacnSender()  # Create and start the sender

    def get_effects(self) -> [EffectInformation]:
        descriptions = []
        for effect in self.EFFECTS:
            descriptions.append(effect.description())

        return descriptions

    def get_selected_effect(self) -> EffectInformation:
        return self.current_effect.description()

    def set_effect(self, position: int):
        try:
            self.current_effect = self.EFFECTS[position]
        except IndexError:
            print(f"Effect at index {position} not found!")

        self.current_effect.start(60)

    def set_color(self, position: int):
        try:
            self.current_color = self.COLORS[position]
        except IndexError:
            print(f"Color-Effect at index {position} not found!")

    def start(self):
        self.set_effect(0)
        self.set_color(0)

        self.worker.start()

    def pause(self):
        pass

    def process(self, raw: np.ndarray):
        signal = self.current_effect.run(raw)
        self.sender.send(self.current_color.visualize(signal))
        self.callback(signal)
