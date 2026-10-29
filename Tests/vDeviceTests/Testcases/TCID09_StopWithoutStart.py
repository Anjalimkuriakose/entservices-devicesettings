"""
/**
 * @file TCID09_StopWithoutStart.py
 * @testcase TCID09_StopWithoutStart  [NEGATIVE / EDGE]
 * @details stopInput(COMPOSITE) with nothing started, repeated three times,
 *          neither crashes nor errors, and start still works afterwards.
 */
"""

import time

from utils import is_ok, log_error
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID09_StopWithoutStart"


def run_test():
    t0 = time.perf_counter()
    try:
        H.cleanup()
        for i in range(3):
            if not is_ok(H.call(Api.stop_input(), f"stopInput (idle) #{i + 1}")):
                log_error(f"{NAME}: idle stopInput #{i + 1} failed")
                return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.start_input(0), "startInput after idle stops")):
            log_error(f"{NAME}: start failed after idle stops")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
