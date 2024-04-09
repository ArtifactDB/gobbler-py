from typing import Optional, Tuple
import appdirs
import platform
import tempfile
import subprocess
import requests
import shutil
import os
import time

test_staging = None
test_registry = None
test_process = None

def start_gobbler(staging: Optional[str] = None, registry: Optional[str] = None, wait: float = 1) -> Tuple[bool, str, str]:
    """
    Start a test gobbler service.

    Args:
        registry: 
            Path to a registry directory. If None, a temporary directory is
            automatically created.

        staging: 
            Path to a registry directory. If None, a temporary directory is
            automatically created.

        wait:
            Number of seconds to wait for the service to initialize before use.

    Returns:
        A tuple indicating whether a new test service was created (or an
        existing instance was re-used), the path to the staging directory, and
        the path to the registry.
    """
    global test_staging
    global test_registry
    global test_process

    if test_process is not None:
        return False, test_staging, test_registry

    exe = _acquire_gobbler_binary()
    _initialize_gobbler_process(exe, staging, registry)

    time.sleep(wait) # give it some time to spin up.
    return True, test_staging, test_registry


def _acquire_gobbler_binary():
    sysname = platform.system()
    if sysname == "Darwin":
        OS = "darwin"
    elif sysname == "Linux":
        OS = "linux"
    else:
        raise ValueError("unsupported operating system '" + sysname + "'")

    sysmachine = platform.machine()
    if sysmachine == "arm64":
        arch = "arm64"
    elif sysmachine == "x86_64":
        arch = "amd64"
    else:
        raise ValueError("unsupported architecture '" + sysmachine + "'")

    cache = appdirs.user_data_dir("gobbler", "aaron")
    desired = "gobbler-" + OS + "-" + arch
    exe = os.path.join(cache, desired)

    if not os.path.exists(exe):
        url = "https://github.com/ArtifactDB/gobbler/releases/download/latest/" + desired

        os.makedirs(cache, exist_ok=True)
        tmp = exe + ".tmp"
        with requests.get(url, stream=True) as r:
            with open(tmp, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        os.chmod(tmp, 0o755)

        # Using a write-and-rename paradigm to provide some atomicity. Note
        # that renaming doesn't work across different filesystems so in that
        # case we just fall back to copying.
        try:
            shutil.move(tmp, exe)
        except:
            shutil.copy(tmp, exe)

    return exe
   

def _initialize_gobbler_process(exe: str, staging: Optional[str], registry: Optional[str]):
    if staging is None:
        staging = tempfile.mkdtemp()
    if registry is None:
        registry = tempfile.mkdtemp()

    global test_staging
    test_staging = staging
    global test_registry
    test_registry = registry

    global test_process
    test_process = subprocess.Popen([ exe, "-admin", os.getlogin(), "-registry", registry, "-staging", staging ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return


def stop_gobbler():
    """
    Stop any existing gobbler test service. This will also reset any URL that
    was modified by :py:func:`~start_gobbler`. If no test service was running,
    this function is a no-op.
    """
    global test_process 
    if test_process is not None:
        test_process.terminate()
        test_process = None
    return
