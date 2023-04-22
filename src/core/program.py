import numpy
import numpy as np
from typing import Optional, Callable

from input import InputStreamThread
import sender

from src.effects.effect import AudioEffect, EffectInformation
from src.effects.melbank import MelbankEffect
from src.effects.spectrum import SpectrumEffect
from src.effects.energy import EnergyEffect

from src.colors.effect import ColorEffect
from src.colors.single import StaticColor


class SingleProgram:
    EFFECTS: list[AudioEffect] = [
        SpectrumEffect(), EnergyEffect(), MelbankEffect()
    ]

    COLORS: list[ColorEffect] = [
        StaticColor()
    ]

    def __init__(self, callback: Callable[[np.ndarray], None] = None):
        """
        Create a new visualization program.
        Provide a callback function if your wish to get the signal output, which will
        be transmitted to the end device

        :param callback: Callback function which accepts the visualized signal
        """

        self.current_color: Optional[ColorEffect] = None
        self.current_effect: Optional[AudioEffect] = None
        self.callback = callback

        self.worker = InputStreamThread(self._process)  # Create a worker thread
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
            self.current_effect.activate(n_led=60, sample_rate=InputStreamThread.SAMPLE_RATE)
        except IndexError:
            print(f"Effect at index {position} not found!")

    def set_color(self, position: int):
        try:
            self.current_color = self.COLORS[position]
            self.current_color.start()
        except IndexError:
            print(f"Color-Effect at index {position} not found!")

    def start(self):
        """
        Start the visualization
        """

        self.set_effect(0)
        self.set_color(0)

        self.worker.start()

    def pause(self):
        pass

    def _process(self, raw: np.ndarray):
        # Process the effect
        signal = self.current_effect.process(raw)

        # If the effect doesn't have a color render function, use the standard color animations instead
        if not self.current_effect.use_color_render:
            signal = self.current_color.visualize(signal)

        self.sender.send(signal)
        self.callback(signal)
