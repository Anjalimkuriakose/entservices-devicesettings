"""
/**
 * @file TCID02_StartStopInput.py
 * @testcase TCID02_StartStopInput  [POSITIVE]
 * @details startInput(portId=0, COMPOSITE) -> onInputStatusChanged "started";
 *          stopInput -> "stopped"; a second stopInput is still successful.
 */
"""

import time

from utils import JsonRpcEventListener, is_ok, log_error, log_info
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID02_StartStopInput"
PORT = 0


def _expect(listener, status):
    note = listener.wait_for_event(
        lambda p: str(p.get("id")) == str(PORT) and p.get("status") == status,
        timeout=H.EVENT_TIMEOUT,
    )
    if note is None:
        log_error(f"{NAME}: onInputStatusChanged '{status}' not received")
    return note is not None


def run_test():
    t0 = time.perf_counter()
    listener = JsonRpcEventListener(Api.CALLSIGN, "onInputStatusChanged", f"ID_{NAME}", timeout=H.EVENT_TIMEOUT)
    if not listener.connect():
        log_error(f"{NAME}: event registration rejected")
        return H.finish(NAME, t0, False)
    try:
        if not is_ok(H.call(Api.start_input(PORT), "startInput")) or not _expect(listener, "started"):
            return H.finish(NAME, t0, False)
        time.sleep(1)
        if not is_ok(H.call(Api.stop_input(), "stopInput")) or not _expect(listener, "stopped"):
            return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.stop_input(), "stopInput (again)")):
            log_error(f"{NAME}: second stopInput not handled")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
        listener.close()
    log_info("start/stop events verified")
    return H.finish(NAME, t0)
