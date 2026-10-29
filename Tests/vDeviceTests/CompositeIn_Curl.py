"""
/**
 * @file CompositeIn_Curl.py
 * @brief org.rdk.AVInput (COMPOSITE) JSON-RPC curl command builders.
 *
 * @details Single source of truth for the composite-input curl commands:
 *          getInputDevices, startInput, stopInput, setVideoRectangle
 *          (all with typeOfInput=COMPOSITE), plus raw builders for negative
 *          / malformed variants.
 */
"""

import json

from utils import WPEFRAMEWORK_JSONRPC_URL

CALLSIGN = "org.rdk.AVInput"
TYPE_COMPOSITE = "COMPOSITE"
TYPE_HDMI = "HDMI"

# Signal status strings delivered by onSignalChanged
SIGNAL_NO = "noSignal"
SIGNAL_UNSTABLE = "unstableSignal"
SIGNAL_NOT_SUPPORTED = "notSupportedSignal"
SIGNAL_STABLE = "stableSignal"


def _curl(method, params=None, timeout=5, request_id=42):
    payload = {"jsonrpc": "2.0", "id": request_id, "method": f"{CALLSIGN}.{method}"}
    if params is not None:
        payload["params"] = params
    return [
        "curl",
        "--max-time", str(timeout),
        "--header", "Content-Type: application/json",
        "--request", "POST",
        "--data", json.dumps(payload),
        WPEFRAMEWORK_JSONRPC_URL,
    ]


def get_input_devices(type_of_input=TYPE_COMPOSITE):
    return _curl("getInputDevices", params={"typeOfInput": type_of_input})


def number_of_inputs():
    return _curl("numberOfInputs")


def start_input(port_id, type_of_input=TYPE_COMPOSITE, timeout=8):
    return _curl(
        "startInput",
        params={"portId": str(port_id), "typeOfInput": type_of_input},
        timeout=timeout,
    )


def stop_input(type_of_input=TYPE_COMPOSITE, timeout=8):
    return _curl("stopInput", params={"typeOfInput": type_of_input}, timeout=timeout)


def set_video_rectangle(x, y, w, h, type_of_input=TYPE_COMPOSITE):
    return _curl(
        "setVideoRectangle",
        params={"x": x, "y": y, "w": w, "h": h, "typeOfInput": type_of_input},
    )


def raw(method, params=None, timeout=5):
    """Arbitrary params dict (malformed / missing / wrong-typed) for negative tests."""
    return _curl(method, params=params, timeout=timeout)
