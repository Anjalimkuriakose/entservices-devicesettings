"""
/**
 * @file TCID17_SignalStatusTransitions.py
 * @testcase TCID17_SignalStatusTransitions  [POSITIVE / YAML-DRIVEN]
 * @details With composite started and connected, injects NO_SIGNAL -> UNSTABLE
 *          -> STABLE via YAML and expects onSignalChanged with noSignal,
 *          unstableSignal, stableSignal in that order.
 */
"""

import time

from utils import JsonRpcEventListener, is_ok, log_error, log_success
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID17_SignalStatusTransitions"
PORT = 0
STEPS = [
    ("CompositeInput_Signal_NOSIGNAL_Status.yaml", Api.SIGNAL_NO),
    ("CompositeInput_Signal_UNSTABLE_Status.yaml", Api.SIGNAL_UNSTABLE),
    ("CompositeInput_Signal_STABLE_Status.yaml", Api.SIGNAL_STABLE),
]


def run_test():
    t0 = time.perf_counter()
    listener = JsonRpcEventListener(Api.CALLSIGN, "onSignalChanged", f"ID_{NAME}", timeout=H.EVENT_TIMEOUT)
    if not listener.connect():
        log_error(f"{NAME}: event registration rejected")
        return H.finish(NAME, t0, False)
    try:
        if not is_ok(H.call(Api.start_input(PORT), "startInput")):
            return H.finish(NAME, t0, False)
        if not H.post_composite("connection_status", {"port": PORT, "connected": True}):
            return H.finish(NAME, t0, False)
        for yaml_name, expected in STEPS:
            if not H.post_composite_file(yaml_name):
                log_error(f"{NAME}: {yaml_name} rejected")
                return H.finish(NAME, t0, False)
            note = listener.wait_for_event(
                lambda p: str(p.get("id")) == str(PORT) and p.get("signalStatus") == expected,
                timeout=H.EVENT_TIMEOUT,
            )
            if note is None:
                log_error(f"{NAME}: onSignalChanged '{expected}' not received")
                return H.finish(NAME, t0, False)
            log_success(f"captured {expected}")
    finally:
        H.post_composite("signal_status", {"port": PORT, "state": "NO_SIGNAL"})
        H.post_composite("connection_status", {"port": PORT, "connected": False})
        H.cleanup()
        listener.close()
    return H.finish(NAME, t0)
