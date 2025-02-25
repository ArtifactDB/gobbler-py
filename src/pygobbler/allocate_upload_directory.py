import os
import tempfile


def allocate_upload_directory(staging: str) -> str:
    """
    Allocate a subdirectory in the staging directory to prepare files for upload via :py:func:`~.upload_directory`.

    Args:
        staging:
            Path to the staging directory.

    Returns:
        Path to a new subdirectory for staging uploads.
    """
    trial = tempfile.mkdtemp(dir=staging)
    # Doing this little shuffle to get the right permissions. tempfile loves to
    # create 0o700 directories that the gobbler service account can't actually
    # read, so we just delete it and create it again under the more permissive
    # umask. Unfortunately we can't use chmod as this screws up FACLs.
    os.rmdir(trial)
    os.mkdir(trial)
    return trial
