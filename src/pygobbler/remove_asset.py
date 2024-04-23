from . import _utils as ut


def remove_asset(project: str, asset: str, staging: str, url: str):
    """
    Remove an asset of a project from the registry.

    Args:
        project:
            The name of the project.

        asset:
            The name of the asset to remove.

        staging:
            Path to the staging directory.

        url:
            URL to the Gobbler REST API.
    """
    ut.dump_request(staging, url, "delete_asset", { "project": project, "asset": asset })
