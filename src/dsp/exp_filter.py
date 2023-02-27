import numpy as np


class SimpleExpFilter:

    def __init__(self, val=0.0, alpha_decay=0.5, alpha_rise=0.5):
        self.alpha_decay = alpha_decay
        self.alpha_rise = alpha_rise
        self.forcast = val

    def update(self, y):
        # Falls der Eingabewert eine Liste ist
        if isinstance(self.forcast, (list, np.ndarray, tuple)):
            # Wert vom Startwert abziehen und schauen, ob er darüber oder darunter liegt
            alpha = y - self.forcast
            alpha[alpha > 0.0] = self.alpha_rise
            alpha[alpha <= 0.0] = self.alpha_decay
        else:
            # Nur für einen Punkt
            alpha = self.alpha_rise if y > self.forcast else self.alpha_decay

        # Simple Exponential Smoothing
        self.forcast = alpha * y + (1.0 - alpha) * self.forcast
        return self.forcast
