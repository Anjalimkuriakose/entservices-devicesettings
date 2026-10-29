"""
/**
 * @file TCID12_DoubleStartSamePort.py
 * @testcase TCID12_DoubleStartSamePort  [EDGE-TO-EDGE]
 * @details startInput twice on the same port without a stop must be answered
 *          both times (no hang / crash); one stopInput then releases the port
 *          and an onInputStatusChanged "stopped" is delivered.
 */
"""

import time

from utils import JsonRpcEventListener, is_ok, log_error, responded
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID12_DoubleStartSamePort"


def run_test():
    t0 = time.perf_counter()
    listener = JsonRpcEventListener(Api.CALLSIGN, "onInputStatusChanged", f"ID_{NAME}", timeout=H.EVENT_TIMEOUT)
    if not listener.connect():
        log_error(f"{NAME}: event registration rejected")
        return H.finish(NAME, t0, False)
    try:
        if not is_ok(H.call(Api.start_input(0), "startInput #1")):
            return H.finish(NAME, t0, False)
        if not responded(H.call(Api.start_input(0), "startInput #2 (same port)")):
            log_error(f"{NAME}: second start unanswered")
            return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.stop_input(), "stopInput")):
            return H.finish(NAME, t0, False)
        note = listener.wait_for_event(lambda p: p.get("status") == "stopped", timeout=H.EVENT_TIMEOUT)
        if note is None:
            log_error(f"{NAME}: 'stopped' event missing after single stop")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
        listener.close()
    return H.finish(NAME, t0)
