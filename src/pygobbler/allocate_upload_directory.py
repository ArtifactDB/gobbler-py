def allocate_upload_directory(staging: str) -> str:
    """
    Allocate a subdirectory in the staging directory to prepare files for
    upload via :py:func:`~.upload_directory`.

    Args:
        staging:
            Path to the staging directory.

    Returns:
        Path to a new subdirectory for staging uploads.
    """
    import tempfile
    return tempfile.mkdtemp(dir=staging)
