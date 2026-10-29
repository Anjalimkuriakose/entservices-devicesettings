"""
/**
 * @file TCID19_DisconnectWhilePresenting.py
 * @testcase TCID19_DisconnectWhilePresenting  [EDGE-TO-EDGE / YAML-DRIVEN]
 * @details Source is unplugged (vComponent connected=false) while the input is
 *          being presented: the plugin must stay responsive, stopInput must
 *          still succeed, and a reconnect + restart works.
 */
"""

import time

from utils import is_ok, log_error
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID19_DisconnectWhilePresenting"
PORT = 0


def run_test():
    t0 = time.perf_counter()
    try:
        if not H.post_composite("connection_status", {"port": PORT, "connected": True}):
            return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.start_input(PORT), "startInput")):
            return H.finish(NAME, t0, False)
        if not H.post_composite("connection_status", {"port": PORT, "connected": False}):
            return H.finish(NAME, t0, False)
        time.sleep(1)
        if not H.healthy():
            log_error(f"{NAME}: plugin unresponsive after unplug")
            return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.stop_input(), "stopInput after unplug")):
            log_error(f"{NAME}: stopInput failed after unplug")
            return H.finish(NAME, t0, False)
        H.post_composite("connection_status", {"port": PORT, "connected": True})
        if not is_ok(H.call(Api.start_input(PORT), "startInput after replug")):
            log_error(f"{NAME}: restart after replug failed")
            return H.finish(NAME, t0, False)
    finally:
        H.post_composite("connection_status", {"port": PORT, "connected": False})
        H.cleanup()
    return H.finish(NAME, t0)
