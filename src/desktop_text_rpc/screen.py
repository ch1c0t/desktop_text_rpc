"""Capture the primary monitor of an X11 display."""

import mss
import numpy as np


def capture_desktop(display=None):
    """Return the selected display's primary monitor as a BGR array."""
    with mss.mss(display=display) as screen:
        pixels = np.asarray(screen.grab(screen.monitors[1]))
    return pixels[:, :, :3].copy()
