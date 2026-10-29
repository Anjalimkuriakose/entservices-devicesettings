"""
/**
 * @file TCID13_HdmiCompositeIsolation.py
 * @testcase TCID13_HdmiCompositeIsolation  [EDGE-TO-EDGE]
 * @details COMPOSITE and HDMI input types are independent: both enumerate,
 *          stopInput(COMPOSITE) while composite is active leaves HDMI
 *          enumeration intact, and stopInput(HDMI) while composite is active
 *          must not release the composite port.
 */
"""

import time

from utils import is_ok, log_error
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID13_HdmiCompositeIsolation"


def run_test():
    t0 = time.perf_counter()
    try:
        hdmi_before = H.parse_devices(H.call(Api.get_input_devices(Api.TYPE_HDMI), "getInputDevices(HDMI)"))
        if not is_ok(H.call(Api.start_input(0), "startInput composite")):
            return H.finish(NAME, t0, False)
        H.call(Api.stop_input(Api.TYPE_HDMI), "stopInput(HDMI) while composite active")
        if not is_ok(H.call(Api.set_video_rectangle(0, 0, 1280, 720), "composite rectangle after HDMI stop")):
            log_error(f"{NAME}: composite released by stopInput(HDMI)")
            return H.finish(NAME, t0, False)
        if not is_ok(H.call(Api.stop_input(), "stopInput composite")):
            return H.finish(NAME, t0, False)
        hdmi_after = H.parse_devices(H.call(Api.get_input_devices(Api.TYPE_HDMI), "getInputDevices(HDMI) after"))
        if hdmi_before != hdmi_after:
            log_error(f"{NAME}: HDMI enumeration changed {hdmi_before} -> {hdmi_after}")
            return H.finish(NAME, t0, False)
    finally:
        H.cleanup()
    return H.finish(NAME, t0)
