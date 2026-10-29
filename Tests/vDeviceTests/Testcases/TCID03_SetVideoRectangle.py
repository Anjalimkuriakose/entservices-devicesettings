"""
/**
 * @file TCID03_SetVideoRectangle.py
 * @testcase TCID03_SetVideoRectangle  [POSITIVE]
 * @details With composite started: full-screen, PIP (quarter screen), moved PIP
 *          and restore to full-screen rectangles are all accepted.
 */
"""

import time

from utils import is_ok, log_error
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID03_SetVideoRectangle"
RECTS = [
    ("full-screen", (0, 0, 1920, 1080)),
    ("PIP", (960, 540, 960, 540)),
    ("PIP moved", (100, 100, 640, 360)),
    ("restore full-screen", (0, 0, 1920, 1080)),
]


def run_test():
    t0 = time.perf_counter()
    try:
        if not is_ok(H.call(Api.start_input(0), "startInput")):
            log_error(f"{NAME}: startInput failed")
            return H.finish(NAME, t0, False)
        for label, rect in RECTS:
            if not is_ok(H.call(Api.set_video_rectangle(*rect), f"setVideoRectangle {label}")):
                log_error(f"{NAME}: {label} rectangle rejected")
                return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
