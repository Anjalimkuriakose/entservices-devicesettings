"""
/**
 * @file CompositeIn_Helpers.py
 * @brief Response parsers, vComponent injection and common check helpers for
 *        the composite-input L3 suite.
 */
"""

import json
import os
import subprocess
import time

from utils import (
    COMPOSITEIN_CMD_BASE,
    COMPOSITEIN_VCOMPONENT_API_URL,
    is_ok,
    log_error,
    log_success,
    log_warning,
    parse_result,
    responded,
    send_curl_command,
    send_vcomponent_command,
)
import CompositeIn_Curl as Api

EVENT_TIMEOUT = float(os.environ.get("AVINPUT_EVENT_TIMEOUT", "8"))


def finish(name, start_time, ok=True):
    elapsed = time.perf_counter() - start_time
    msg = f"{name} {'Passed ✅' if ok else 'Failed ❌'}"
    if ok and os.environ.get("AVINPUT_TIMING_ENABLED"):
        log_success(f"{msg} time consumed: {elapsed:.3f}s")
    elif ok:
        log_success(msg)
    else:
        log_error(msg)
    return ok


def call(cmd, label=None):
    resp = send_curl_command(cmd)
    log_warning(f"{label or cmd[-3][:60]} -> {resp}")
    return resp


def has_error(resp):
    """True for a JSON-RPC error object or a plugin-level success:false."""
    if not responded(resp):
        return False
    try:
        body = json.loads(resp)
    except json.JSONDecodeError:
        return False
    if not isinstance(body, dict):
        return False
    if "error" in body:
        return True
    result = body.get("result")
    return isinstance(result, dict) and result.get("success") is False


def parse_devices(resp):
    result = parse_result(resp)
    if not isinstance(result, dict):
        return None
    devices = result.get("devices")
    if not isinstance(devices, list):
        devices = result.get("deviceList")
    return devices if isinstance(devices, list) else None


def device_connected(devices, port):
    for dev in devices or []:
        if isinstance(dev, dict) and str(dev.get("id")) == str(port):
            return dev.get("connected")
    return None


def composite_ports():
    """Return the list of composite port ids reported by getInputDevices."""
    devices = parse_devices(call(Api.get_input_devices(), "getInputDevices(COMPOSITE)"))
    if not devices:
        return []
    return [int(d["id"]) for d in devices if isinstance(d, dict) and str(d.get("id")).lstrip("-").isdigit()]


def healthy():
    """Plugin still answers a valid composite query."""
    return is_ok(call(Api.get_input_devices(), "health getInputDevices"))


def cleanup():
    send_curl_command(Api.stop_input())


def post_composite(command, params):
    """Post one composite-input command to the vComponent. Returns True when accepted."""
    payload = {"compositeinput": {"command": command, "params": params}}
    cmd = [
        "curl", "-sS", "--max-time", "5", "-w", "\n%{http_code}",
        "-X", "POST", "-H", "Content-Type: application/x-yaml",
        "--data-binary", "@-", COMPOSITEIN_VCOMPONENT_API_URL,
    ]
    res = subprocess.run(cmd, input=json.dumps(payload), check=False, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    body, _, code = (res.stdout or "").rpartition("\n")
    try:
        http = int(code.strip())
    except ValueError:
        http = 0
    # Some vComponent builds apply the command and close without replying.
    if http == 0 and res.returncode == 52:
        http = 200
    log_warning(f"vComponent {command}{params}: HTTP {http} {body or res.stderr.strip()}")
    return http == 200


def post_composite_file(yaml_name):
    code, body = send_vcomponent_command(f"{COMPOSITEIN_CMD_BASE}/{yaml_name}")
    log_warning(f"vComponent POST {yaml_name}: HTTP {code} {body}")
    return code == 200
