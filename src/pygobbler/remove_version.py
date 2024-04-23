from . import _utils as ut


def remove_version(project: str, asset: str, version: str, staging: str, url: str):
    """
    Remove a version of a project asset from the registry.

    Args:
        project:
            The name of the project.

        asset:
            The name of the asset of the ``project`..

        version:
            The name of the version of the ``asset`` to remove.

        staging:
            Path to the staging directory.

        url:
            URL to the Gobbler REST API.
    """
    ut.dump_request(staging, url, "delete_version", { "project": project, "asset": asset, "version": version })
