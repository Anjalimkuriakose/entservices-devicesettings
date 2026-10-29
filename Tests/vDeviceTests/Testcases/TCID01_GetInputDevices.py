"""
/**
 * @file TCID01_GetInputDevices.py
 * @testcase TCID01_GetInputDevices  [POSITIVE]
 * @details getInputDevices(COMPOSITE) succeeds and every entry has a unique
 *          id, a locator string and a boolean connected flag.
 */
"""

import time

from utils import is_ok, log_error, log_info
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID01_GetInputDevices"


def run_test():
    t0 = time.perf_counter()
    resp = H.call(Api.get_input_devices(), "getInputDevices(COMPOSITE)")
    if not is_ok(resp):
        log_error(f"{NAME}: getInputDevices did not succeed")
        return H.finish(NAME, t0, False)
    devices = H.parse_devices(resp)
    if not devices:
        log_error(f"{NAME}: empty/missing device list")
        return H.finish(NAME, t0, False)
    ids = []
    for dev in devices:
        if not (isinstance(dev, dict) and "id" in dev and isinstance(dev.get("locator"), str)
                and isinstance(dev.get("connected"), bool)):
            log_error(f"{NAME}: malformed device entry {dev}")
            return H.finish(NAME, t0, False)
        ids.append(str(dev["id"]))
    if len(set(ids)) != len(ids):
        log_error(f"{NAME}: duplicate port ids {ids}")
        return H.finish(NAME, t0, False)
    log_info(f"Composite ports: {ids}")
    return H.finish(NAME, t0)
