from typing import Optional, Dict, List
import json
import os
import tempfile
import requests


def format_error(res):
    ctype = res.headers["content-type"]
    if ctype == "application/json":
        info = res.json()
        return requests.HTTPError(res.status_code, info["reason"])
    elif ctype == "text/plain":
        return requests.HTTPError(res.status_code, res.text)
    else:
        return requests.HTTPError(res.status_code)


def dump_request(staging: str, url: str, action: str, payload: Optional[Dict]) -> str:
    if payload is None:
        as_str = character(0)
    else:
        as_str = json.dumps(payload, indent=4)

    prefix = "request-" + action + "-"
    fd, holding_name = tempfile.mkstemp(dir=staging, prefix=prefix)
    with os.fdopen(fd, "w") as handle:
        handle.write(as_str)

    res = requests.post(url + "/new/" + os.path.basename(holding_name))
    if res.status_code >= 300:
        raise format_error(res)

    return res.json()
