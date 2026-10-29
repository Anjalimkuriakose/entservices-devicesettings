"""
/**
 * @file TCID07_InvalidTypeOfInput.py
 * @testcase TCID07_InvalidTypeOfInput  [NEGATIVE]
 * @details Unknown / empty / wrong-case / wrong-type typeOfInput on
 *          getInputDevices, startInput, stopInput and setVideoRectangle gets a
 *          response (never a hang/crash); unknown values are rejected on
 *          getInputDevices and startInput. Plugin stays healthy.
 */
"""

import time

from utils import log_error, responded
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID07_InvalidTypeOfInput"
REJECTED = ["ABCD", "", "COMPOSITE1", 123]
TOLERATED = ["composite", "Composite", " COMPOSITE"]


def _calls(t):
    return [
        ("getInputDevices", Api.raw("getInputDevices", {"typeOfInput": t})),
        ("startInput", Api.raw("startInput", {"portId": "0", "typeOfInput": t})),
        ("stopInput", Api.raw("stopInput", {"typeOfInput": t})),
        ("setVideoRectangle", Api.raw("setVideoRectangle", {"x": 0, "y": 0, "w": 1920, "h": 1080, "typeOfInput": t})),
    ]


def run_test():
    t0 = time.perf_counter()
    try:
        for t in REJECTED + TOLERATED:
            for method, cmd in _calls(t):
                resp = H.call(cmd, f"{method} typeOfInput={t!r}")
                if not responded(resp):
                    log_error(f"{NAME}: no response {method} typeOfInput={t!r}")
                    return H.finish(NAME, t0, False)
                if t in REJECTED and method in ("getInputDevices", "startInput") and not H.has_error(resp):
                    log_error(f"{NAME}: {method} accepted typeOfInput={t!r}")
                    return H.finish(NAME, t0, False)
        resp = H.call(Api.raw("startInput", {"portId": "0"}), "startInput missing typeOfInput")
        if not responded(resp):
            return H.finish(NAME, t0, False)
        if not H.healthy():
            log_error(f"{NAME}: plugin unhealthy afterwards")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
