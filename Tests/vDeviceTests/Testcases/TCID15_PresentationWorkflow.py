"""
/**
 * @file TCID15_PresentationWorkflow.py
 * @testcase TCID15_PresentationWorkflow  [POSITIVE / SCENARIO]
 * @details Journey: enumerate -> start -> full-screen -> PIP -> move -> restore
 *          -> stop -> rectangle after stop is handled -> enumerate again.
 */
"""

import time

from utils import is_ok, log_error, responded
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID15_PresentationWorkflow"


def run_test():
    t0 = time.perf_counter()
    ports = H.composite_ports()
    if not ports:
        log_error(f"{NAME}: no composite ports")
        return H.finish(NAME, t0, False)
    port = ports[0]
    try:
        steps = [
            ("start", Api.start_input(port)),
            ("full-screen", Api.set_video_rectangle(0, 0, 1920, 1080)),
            ("PIP", Api.set_video_rectangle(1280, 720, 640, 360)),
            ("PIP moved", Api.set_video_rectangle(0, 0, 640, 360)),
            ("restore", Api.set_video_rectangle(0, 0, 1920, 1080)),
            ("stop", Api.stop_input()),
        ]
        for label, cmd in steps:
            if not is_ok(H.call(cmd, label)):
                log_error(f"{NAME}: step '{label}' failed")
                return H.finish(NAME, t0, False)
        if not responded(H.call(Api.set_video_rectangle(0, 0, 1920, 1080), "rectangle after stop")):
            return H.finish(NAME, t0, False)
        if H.composite_ports() != ports:
            log_error(f"{NAME}: port list changed")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
