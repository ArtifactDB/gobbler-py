from . import _utils as ut


def reject_probation(project: str, asset: str, version: str, staging: str, url: str):
    """
    Reject a probational upload of a version of a project's asset.

    Args:
        project:
            The name of the project.

        asset:
            The name of the asset of the ``project``.

        version:
            The name of the version of the ``asset`` to reject.

        staging:
            Path to the staging directory.

        url:
            URL to the Gobbler REST API.
    """
    ut.dump_request(staging, url, "reject_probation", { "project": project, "asset": asset, "version": version })
