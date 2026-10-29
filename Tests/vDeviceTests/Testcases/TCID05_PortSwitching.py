"""
/**
 * @file TCID05_PortSwitching.py
 * @testcase TCID05_PortSwitching  [POSITIVE / SCENARIO]
 * @details Direct switching between all composite ports without an intervening
 *          stop, then a single stop releases the active port. Single-port
 *          devices only verify re-start of the same port.
 */
"""

import time

from utils import is_ok, log_error, log_info
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID05_PortSwitching"


def run_test():
    t0 = time.perf_counter()
    ports = H.composite_ports() or [0]
    if len(ports) < 2:
        log_info("Single composite port: verifying same-port restart only")
        ports = ports * 2
    try:
        for port in ports + ports[::-1]:
            if not is_ok(H.call(Api.start_input(port), f"startInput port={port}")):
                log_error(f"{NAME}: switch to port {port} failed")
                return H.finish(NAME, t0, False)
            time.sleep(0.5)
        if not is_ok(H.call(Api.stop_input(), "stopInput")):
            log_error(f"{NAME}: stop after switching failed")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
