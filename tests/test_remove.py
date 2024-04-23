import pygobbler as pyg
import tempfile
import os
import time

_, staging, registry, url = pyg.start_gobbler()

pyg.remove_project("test-R-remove", staging=staging, url=url)
pyg.create_project("test-R-remove", staging=staging, url=url)

src = pyg.allocate_upload_directory(staging)
pyg.upload_directory("test-R-remove", "sacrifice", "v1", src, staging=staging, url=url)
time.sleep(1.1) # force timestamps to be different for next versions.
pyg.upload_directory("test-R-remove", "sacrifice", "v2", src, staging=staging, url=url)


def test_remove_version():
    assert os.path.exists(os.path.join(registry, "test-R-remove", "sacrifice", "v2"))
    pyg.remove_version("test-R-remove", "sacrifice", "v2", staging=staging, url=url)
    assert not os.path.exists(os.path.join(registry, "test-R-remove", "sacrifice", "v2"))


def test_remove_asset():
    assert os.path.exists(os.path.join(registry, "test-R-remove", "sacrifice"))
    pyg.remove_asset("test-R-remove", "sacrifice", staging=staging, url=url)
    assert not os.path.exists(os.path.join(registry, "test-R-remove", "sacrifice"))


def test_remove_project():
    assert os.path.exists(os.path.join(registry, "test-R-remove"))
    pyg.remove_project("test-R-remove", staging=staging, url=url)
    assert not os.path.exists(os.path.join(registry, "test-R-remove"))
