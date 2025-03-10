from typing import Optional, List
from . import _utils as ut
from . import fetch_permissions


def set_permissions(
    project: str,
    registry: str,
    staging: str,
    url: str,
    asset: Optional[str] = None,
    owners: Optional[List] = None,
    uploaders: Optional[List] = None,
    global_write: Optional[bool] = None,
    append: bool = True,
):
    """
    Set the owner and uploader permissions for a project or an asset within a project.

    Args:
        project:
            Name of the project.

        registry:
            Path to the Gobbler registry.

        staging:
            Path to the staging directory.

        url:
            URL to the Gobbler REST API.

        asset:
            Name of the asset inside the project.
            If supplied, permissions are set on this asset rather than the entire project.

        owners:
            List of user IDs for owners of this project.
            If ``None``, no change is made to the existing owners in the project permissions.

        uploaders:
            List of dictionaries specifying the authorized uploaders for this project.
            Each dictionary should follow the same format as the ``uploaders`` field in the return value of :py:func:`~gobbler.fetch_permissions.fetch_permissions`. 
            If ``None``, no change is made to the existing uploaders.

        global_write:
            Whether to enable global writes for this project, see the ``global_write`` field in the return value of :py:func:`~gobbler.fetch_permissions.fetch_permissions` for more details.
            If ``None``, no change is made to the global write status.
            Ignored if ``asset`` is provided.

        append:
            Whether ``owners`` and ``uploaders`` should be appended to the existing owners and uploaders, respectively.
            If ``False``, the ``owners`` and ``uploaders`` are used to replace the existing values in the project permissions.
    """
    perms = {}

    if append:
        oldperms = fetch_permissions(project, asset=asset, registry=registry, url=url)
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

    payload = { "project": project }
    if asset is not None:
        payload["asset"] = asset
    elif global_write is not None:
        perms["global_write"] = global_write

    payload["permissions"] = perms
    ut.dump_request(staging, url, "set_permissions", payload)
