from typing import Optional, Dict
import json
import os
import tempfile
import time


def dump_request(staging: str, action: str, payload: Optional[Dict]) -> str:
    if payload is None:
        as_str = character(0)
    else:
        as_str = json.dumps(payload, indent=4)

    prefix = "request-" + action + "-"
    fd, holding_name = tempfile.mkstemp(dir=staging, prefix=prefix)
    with os.fdopen(fd, "w") as handle:
        handle.write(as_str)

    return os.path.basename(holding_name)


def wait_response(staging: str, request_name: str, error: bool = True, timeout: float = 10):
    target = os.path.join(staging, "responses", request_name)

    start = time.time()
    while not os.path.exists(target):
        if time.time() - start > timeout:
            if error:
                raise ValueError("timed out waiting for a response to '" + request_name + "'")
            return False
        time.sleep(0.2)

    if not error:
        return True

    with open(target, "r") as handle: 
        output = json.load(handle)
    if output["status"] == "FAILED":
        raise ValueError(output["reason"])
    return output
