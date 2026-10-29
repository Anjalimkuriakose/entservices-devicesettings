"""
/**
 * @file TCID14_RapidStartStopStress.py
 * @testcase TCID14_RapidStartStopStress  [EDGE-TO-EDGE / STRESS]
 * @details 25 back-to-back start/rectangle/stop iterations with no delay; every
 *          call must succeed and the plugin must remain healthy.
 */
"""

import time

from utils import is_ok, log_error
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID14_RapidStartStopStress"
ITERATIONS = 25


def run_test():
    t0 = time.perf_counter()
    try:
        for i in range(ITERATIONS):
            steps = (
                ("startInput", Api.start_input(0)),
                ("setVideoRectangle", Api.set_video_rectangle(0, 0, 1920, 1080)),
                ("stopInput", Api.stop_input()),
            )
            for label, cmd in steps:
                if not is_ok(H.call(cmd, f"{label} iter={i + 1}")):
                    log_error(f"{NAME}: {label} failed at iteration {i + 1}")
                    return H.finish(NAME, t0, False)
        if not H.healthy():
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
