"""
/**
 * @file TCID06_InvalidPortId.py
 * @testcase TCID06_InvalidPortId  [NEGATIVE]
 * @details startInput(COMPOSITE) with non-numeric, empty, negative, out-of-range
 *          and missing portId is rejected (JSON-RPC error or success:false);
 *          afterwards a valid start/stop still works.
 */
"""

import time

from utils import is_ok, log_error, responded
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID06_InvalidPortId"
CASES = [
    ("non-numeric 'abc'", {"portId": "abc", "typeOfInput": "COMPOSITE"}),
    ("empty string", {"portId": "", "typeOfInput": "COMPOSITE"}),
    ("negative -1", {"portId": "-1", "typeOfInput": "COMPOSITE"}),
    ("out-of-range 10", {"portId": "10", "typeOfInput": "COMPOSITE"}),
    ("huge 99999999999", {"portId": "99999999999", "typeOfInput": "COMPOSITE"}),
    ("float 0.5", {"portId": "0.5", "typeOfInput": "COMPOSITE"}),
    ("null", {"portId": None, "typeOfInput": "COMPOSITE"}),
    ("missing portId", {"typeOfInput": "COMPOSITE"}),
    ("missing params object", None),
]


def run_test():
    t0 = time.perf_counter()
    try:
        for label, params in CASES:
            resp = H.call(Api.raw("startInput", params), f"startInput {label}")
            if not responded(resp):
                log_error(f"{NAME}: no response for {label}")
                return H.finish(NAME, t0, False)
            if not H.has_error(resp):
                log_error(f"{NAME}: {label} was not rejected")
                return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.start_input(0), "startInput valid")) or \
                not is_ok(H.call(Api.stop_input(), "stopInput valid")):
            log_error(f"{NAME}: plugin unusable after invalid ports")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
