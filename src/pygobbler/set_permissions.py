from typing import Optional, List, Dict
from . import _utils as ut
from . import fetch_permissions


def set_permissions(project: str, registry: str, staging: str, url: str, owners: Optional[List] = None, uploaders: Optional[Dict] = None, append: bool = True):
    """
    Set the owner and uploader permissions for a project.

    Args:
        project:
            Name of the project.

        registry:
            Path to the Gobbler registry.

        staging:
            Path to the staging directory.

        url:
            URL of the REST API.

        owners:
            List of user IDs for owners of this project. If None, no change is
            made to the existing owners in the project permissions.

        uploaders:
            List of dictionaries specifying the authorized uploaders for this
            project.  See the ``uploaders`` field in the return value of
            :py:func:`~fetch_permissions.fetch_permissions` for  the expected
            format. If None, no change is made to the existing uploaders.

        append:
            Whether ``owners`` and ``uploaders`` should be appended to the
            existing owners and uploaders, respectively. If False, the
            ``owners`` and ``uploaders`` are used to replace the existing
            values in the project permissions.
    """
    perms = {}

    if append:
        oldperms = fetch_permissions(project, registry=registry, url=url)
        if owners is not None:
            oldset = set(oldperms["owners"])
            perms["owners"] = oldperms["owners"] + list(filter(lambda x : x not in oldset, owners))
        if uploaders is not None:
            perms["uploaders"] = oldperms["uploaders"] + uploaders
    else:
        if owners is not None:
            perms["owners"] = owners
        if uploaders is not None:
            perms["uploaders"] = uploaders

    ut.dump_request(staging, url, "set_permissions", { "project": project, "permissions": perms })
