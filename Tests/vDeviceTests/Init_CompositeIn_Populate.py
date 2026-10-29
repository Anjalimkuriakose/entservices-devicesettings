"""
/**
 * @file Init_CompositeIn_Populate.py
 * @brief Baseline for every composite-input testcase: verifies the plugin
 *        answers getInputDevices(COMPOSITE) and releases any active port.
 */
"""

import time

from utils import log_error, log_info, log_success
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H


def run_test():
    log_info("CompositeIn suite initialization")
    resp = H.call(Api.get_input_devices(), "getInputDevices(COMPOSITE)")
    if H.parse_devices(resp) is None:
        log_error("Init failed: getInputDevices(COMPOSITE) returned no device list")
        return False
    H.cleanup()
    time.sleep(1)
    log_success("Suite initialization completed successfully")
    return True
