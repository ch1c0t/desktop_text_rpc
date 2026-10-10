"""Capture the primary desktop monitor."""

import mss
import numpy as np


def capture_desktop():
    """Return the primary monitor as a BGR NumPy array."""
    with mss.mss() as screen:
        pixels = np.asarray(screen.grab(screen.monitors[1]))
    return pixels[:, :, :3].copy()
