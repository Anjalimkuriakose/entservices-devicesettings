"""
/**
 * @file TCID04_StartStopCycle.py
 * @testcase TCID04_StartStopCycle  [POSITIVE / REPEATABILITY]
 * @details Five start->stop cycles on every composite port all succeed and the
 *          port list is unchanged afterwards.
 */
"""

import time

from utils import is_ok, log_error
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID04_StartStopCycle"
CYCLES = 5


def run_test():
    t0 = time.perf_counter()
    ports = H.composite_ports() or [0]
    try:
        for port in ports:
            for i in range(CYCLES):
                if not is_ok(H.call(Api.start_input(port), f"startInput port={port} #{i + 1}")):
                    log_error(f"{NAME}: start failed port={port} cycle={i + 1}")
                    return H.finish(NAME, t0, False)
                if not is_ok(H.call(Api.stop_input(), f"stopInput port={port} #{i + 1}")):
                    log_error(f"{NAME}: stop failed port={port} cycle={i + 1}")
                    return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    after = H.composite_ports()
    if after and after != ports:
        log_error(f"{NAME}: port list changed after cycles")
        return H.finish(NAME, t0, False)
    return H.finish(NAME, t0)
