"""
/**
 * @file TCID08_InvalidRectangle.py
 * @testcase TCID08_InvalidRectangle  [NEGATIVE]
 * @details setVideoRectangle with missing fields or wrong types is rejected;
 *          negative / zero dimensions get a response (HAL decides); plugin
 *          stays healthy and a valid rectangle still works.
 */
"""

import time

from utils import is_ok, log_error, responded
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID08_InvalidRectangle"
T = "COMPOSITE"
MUST_REJECT = [
    ("missing x", {"y": 0, "w": 1920, "h": 1080, "typeOfInput": T}),
    ("missing w", {"x": 0, "y": 0, "h": 1080, "typeOfInput": T}),
    ("missing all", {"typeOfInput": T}),
    ("string x", {"x": "a", "y": 0, "w": 1920, "h": 1080, "typeOfInput": T}),
    ("string w", {"x": 0, "y": 0, "w": "wide", "h": 1080, "typeOfInput": T}),
    ("null h", {"x": 0, "y": 0, "w": 1920, "h": None, "typeOfInput": T}),
    ("bool y", {"x": 0, "y": True, "w": 1920, "h": 1080, "typeOfInput": T}),
]
MUST_RESPOND = [
    ("negative x/y", {"x": -10, "y": -10, "w": 1920, "h": 1080, "typeOfInput": T}),
    ("negative w/h", {"x": 0, "y": 0, "w": -1920, "h": -1080, "typeOfInput": T}),
    ("zero w/h", {"x": 0, "y": 0, "w": 0, "h": 0, "typeOfInput": T}),
    ("float values", {"x": 0.5, "y": 0.5, "w": 1920.5, "h": 1080.5, "typeOfInput": T}),
]


def run_test():
    t0 = time.perf_counter()
    try:
        if not is_ok(H.call(Api.start_input(0), "startInput")):
            log_error(f"{NAME}: startInput failed")
            return H.finish(NAME, t0, False)
        for label, params in MUST_REJECT:
            resp = H.call(Api.raw("setVideoRectangle", params), f"setVideoRectangle {label}")
            if not responded(resp) or not H.has_error(resp):
                log_error(f"{NAME}: {label} not rejected")
                return H.finish(NAME, t0, False)
        for label, params in MUST_RESPOND:
            if not responded(H.call(Api.raw("setVideoRectangle", params), f"setVideoRectangle {label}")):
                log_error(f"{NAME}: no response for {label}")
                return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.set_video_rectangle(0, 0, 1920, 1080), "valid rectangle after negatives")):
            log_error(f"{NAME}: valid rectangle rejected after invalid ones")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
