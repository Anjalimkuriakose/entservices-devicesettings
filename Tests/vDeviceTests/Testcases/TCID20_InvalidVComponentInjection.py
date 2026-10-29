"""
/**
 * @file TCID20_InvalidVComponentInjection.py
 * @testcase TCID20_InvalidVComponentInjection  [NEGATIVE / YAML-DRIVEN]
 * @details Out-of-range port, unknown signal state and unknown command posted
 *          to the vComponent must not crash the plugin: getInputDevices and a
 *          start/stop cycle still succeed afterwards.
 */
"""

import time

from utils import is_ok, log_error
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID20_InvalidVComponentInjection"


def run_test():
    t0 = time.perf_counter()
    try:
        H.post_composite("connection_status", {"port": 99, "connected": True})
        H.post_composite("connection_status", {"port": -1, "connected": True})
        H.post_composite("signal_status", {"port": 0, "state": "BOGUS_STATE"})
        H.post_composite("no_such_command", {"port": 0})
        time.sleep(1)
        if not H.healthy():
            log_error(f"{NAME}: plugin unhealthy after invalid injections")
            return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.start_input(0), "startInput")) or not is_ok(H.call(Api.stop_input(), "stopInput")):
            log_error(f"{NAME}: start/stop broken after invalid injections")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
