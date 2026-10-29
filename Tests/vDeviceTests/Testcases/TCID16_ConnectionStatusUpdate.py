"""
/**
 * @file TCID16_ConnectionStatusUpdate.py
 * @testcase TCID16_ConnectionStatusUpdate  [POSITIVE / YAML-DRIVEN]
 * @details Injects composite hot-plug connect (CompositeInput_Connection_Status.yaml)
 *          and disconnect (inline payload) via the vComponent for each port;
 *          onDevicesChanged and getInputDevices(COMPOSITE) must both track it.
 */
"""

import time

from utils import JsonRpcEventListener, is_ok, log_error, log_success
import CompositeIn_Curl as Api
import CompositeIn_Helpers as H

NAME = "TCID16_ConnectionStatusUpdate"
YAML = "CompositeInput_Connection_Status.yaml"


def _connected(port):
    return H.device_connected(H.parse_devices(H.call(Api.get_input_devices(), "getInputDevices")), port)


def _inject(port, state):
    if port == 0 and state:
        return H.post_composite_file(YAML)
    return H.post_composite("connection_status", {"port": port, "connected": state})


def run_test():
    t0 = time.perf_counter()
    ports = H.composite_ports() or [0]
    listener = JsonRpcEventListener(Api.CALLSIGN, "onDevicesChanged", f"ID_{NAME}", timeout=H.EVENT_TIMEOUT)
    if not listener.connect():
        log_error(f"{NAME}: event registration rejected")
        return H.finish(NAME, t0, False)
    try:
        for port in ports:
            # Hot-plug callbacks are delivered only for the opened (started) port
            if not is_ok(H.call(Api.start_input(port), f"startInput port={port}")):
                log_error(f"{NAME}: startInput failed port={port}")
                return H.finish(NAME, t0, False)
            for state in (True, False):
                if not _inject(port, state):
                    log_error(f"{NAME}: injection rejected port={port} connected={state}")
                    return H.finish(NAME, t0, False)
                note = listener.wait_for_event(
                    lambda p: H.device_connected(p.get("devices"), port) is state,
                    timeout=H.EVENT_TIMEOUT,
                )
                if note is None:
                    log_error(f"{NAME}: onDevicesChanged missing port={port} connected={state}")
                    return H.finish(NAME, t0, False)
                if _connected(port) is not state:
                    log_error(f"{NAME}: getInputDevices does not reflect connected={state} port={port}")
                    return H.finish(NAME, t0, False)
                log_success(f"port {port} connected={state} verified")
    finally:
        H.cleanup()
        for port in ports:
            H.post_composite("connection_status", {"port": port, "connected": False})
        listener.close()
    return H.finish(NAME, t0)
