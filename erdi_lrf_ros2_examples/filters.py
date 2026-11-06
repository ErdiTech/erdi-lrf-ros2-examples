"""Pure-Python range filters (no ROS imports) so they can be unit-tested anywhere."""
import math
from collections import deque
from typing import Deque, Optional


class MedianFilter:
    """Sliding-window median that ignores NaN / out-of-range samples."""

    def __init__(self, window: int = 5):
        if window < 1 or window % 2 == 0:
            raise ValueError("window must be a positive odd number")
        self.window = window
        self._buf: Deque[float] = deque(maxlen=window)

    def update(self, value: Optional[float]) -> Optional[float]:
        if value is None or math.isnan(value) or math.isinf(value):
            return self.value()
        self._buf.append(float(value))
        return self.value()

    def value(self) -> Optional[float]:
        if not self._buf:
            return None
        s = sorted(self._buf)
        return s[len(s) // 2]


class SlewLimiter:
    """Reject jumps larger than max_rate m/s: a single-point laser can briefly lock onto a branch or a bird."""

    def __init__(self, max_rate: float = 50.0):
        self.max_rate = max_rate
        self._last: Optional[float] = None
        self._t: Optional[float] = None

    def update(self, value: float, t: float) -> Optional[float]:
        if self._last is None:
            self._last, self._t = value, t
            return value
        dt = max(t - self._t, 1e-6)
        if abs(value - self._last) / dt > self.max_rate:
            return None
        self._last, self._t = value, t
        return value
