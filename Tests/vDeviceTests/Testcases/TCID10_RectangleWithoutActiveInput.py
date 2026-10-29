"""
/**
 * @file TCID10_RectangleWithoutActiveInput.py
 * @testcase TCID10_RectangleWithoutActiveInput  [NEGATIVE / EDGE]
 * @details setVideoRectangle before any startInput and after stopInput gets a
 *          well-formed response and does not break a following start/rectangle.
 */
"""

import time

from utils import is_ok, log_error, responded
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID10_RectangleWithoutActiveInput"
RECT = (0, 0, 1920, 1080)


def run_test():
    t0 = time.perf_counter()
    try:
        H.cleanup()
        if not responded(H.call(Api.set_video_rectangle(*RECT), "setVideoRectangle (never started)")):
            log_error(f"{NAME}: no response before start")
            return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.start_input(0), "startInput")):
            return H.finish(NAME, t0, False)
        H.call(Api.stop_input(), "stopInput")
        if not responded(H.call(Api.set_video_rectangle(*RECT), "setVideoRectangle (after stop)")):
            log_error(f"{NAME}: no response after stop")
            return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.start_input(0), "startInput again")) or \
                not is_ok(H.call(Api.set_video_rectangle(*RECT), "setVideoRectangle (active)")):
            log_error(f"{NAME}: cannot recover after out-of-state rectangle calls")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
