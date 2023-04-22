import numpy as np


class ColorTransition:
    """
    Transforms color transitions.
    If no transition is going on, the static color will be returned
    """

    def __init__(self, color: tuple[int, int, int], transition_time: int):
        """
        Create a new color transition
        :param color: The static color
        :param transition_time: The maximum ticks of the transition
        """

        self.color = color
        self.transition_time = transition_time

        self.transition = None
        self.step = 0

    def change_color(self, new_color: tuple[int, int, int]):
        """
        Change the current color and start a new transition
        """
        step_size = np.subtract(self.color, new_color) / self.transition_time
        self.transition = tuple(step_size)

        self.step = 0

    def change_transition_time(self, new_transition_time):
        """
        Change the maximum amount of ticks needed for an transition
        """
        self.transition_time = new_transition_time

    def update(self) -> tuple[int, int, int]:
        """
        Update and get the current color value
        """

        # Reset the transition, if it reached the end
        if self.step > self.transition_time:
            self.step = 0
            self.transition = None

        # Update the transition if any is going on
        if self.transition is not None:
            self.color = np.add(
                self.color,
                self.transition
            )
            self.step += 1
            print(f"Color transition update: {self.color}")

        return self.color
