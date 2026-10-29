"""
/**
 * @file TCID11_BoundaryRectangle.py
 * @testcase TCID11_BoundaryRectangle  [EDGE-TO-EDGE]
 * @details Boundary geometry: 1x1 window, 4K full plane, window partly or fully
 *          off-screen, INT32_MAX values. 1x1 and 4K must succeed; all others
 *          must be answered and leave the plugin healthy.
 */
"""

import time

from utils import is_ok, log_error, responded
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID11_BoundaryRectangle"
MUST_SUCCEED = [
    ("1x1 at origin", (0, 0, 1, 1)),
    ("1080p full", (0, 0, 1920, 1080)),
    ("4K full", (0, 0, 3840, 2160)),
]
MUST_RESPOND = [
    ("bottom-right corner 1x1", (1919, 1079, 1, 1)),
    ("partially off-screen", (1500, 800, 1920, 1080)),
    ("fully off-screen", (5000, 5000, 640, 360)),
    ("INT32_MAX", (2147483647, 2147483647, 2147483647, 2147483647)),
    ("INT32_MAX+1", (2147483648, 0, 1920, 1080)),
]


def run_test():
    t0 = time.perf_counter()
    try:
        if not is_ok(H.call(Api.start_input(0), "startInput")):
            return H.finish(NAME, t0, False)
        for label, rect in MUST_SUCCEED:
            if not is_ok(H.call(Api.set_video_rectangle(*rect), f"setVideoRectangle {label}")):
                log_error(f"{NAME}: {label} rejected")
                return H.finish(NAME, t0, False)
        for label, rect in MUST_RESPOND:
            if not responded(H.call(Api.set_video_rectangle(*rect), f"setVideoRectangle {label}")):
                log_error(f"{NAME}: no response for {label}")
                return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.set_video_rectangle(0, 0, 1920, 1080), "restore")) or not H.healthy():
            log_error(f"{NAME}: not healthy after boundary values")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
