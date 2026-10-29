"""
/**
 * @file TCID18_VideoModeUpdate.py
 * @testcase TCID18_VideoModeUpdate  [POSITIVE / YAML-DRIVEN]
 * @details With composite started, injects an NTSC 480i video mode via
 *          CompositeInput_VideoMode_Update.yaml; AVInput.currentVideoMode must
 *          answer and, once a mode is injected, report a non-empty string.
 */
"""

import time

from utils import is_ok, log_error, log_info, parse_result
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID18_VideoModeUpdate"


def run_test():
    t0 = time.perf_counter()
    try:
        if not is_ok(H.call(Api.start_input(0), "startInput")):
            return H.finish(NAME, t0, False)
        H.post_composite("connection_status", {"port": 0, "connected": True})
        if not H.post_composite_file("CompositeInput_VideoMode_Update.yaml"):
            log_error(f"{NAME}: video mode injection rejected")
            return H.finish(NAME, t0, False)
        time.sleep(1)
        resp = H.call(Api._curl("currentVideoMode"), "currentVideoMode")
        result = parse_result(resp)
        if not is_ok(resp) or not isinstance(result.get("currentVideoMode"), str):
            log_error(f"{NAME}: currentVideoMode malformed")
            return H.finish(NAME, t0, False)
        if not result["currentVideoMode"]:
            log_error(f"{NAME}: currentVideoMode empty after video mode injection")
            return H.finish(NAME, t0, False)
        log_info(f"currentVideoMode = {result['currentVideoMode']}")
    finally:
        H.post_composite("connection_status", {"port": 0, "connected": False})
        H.cleanup()
    return H.finish(NAME, t0)
