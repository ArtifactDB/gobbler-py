import pygobbler as pyg
import tempfile
import os

_, staging, registry, url = pyg.start_gobbler()
pyg.remove_project("test", staging=staging, url=url)
pyg.create_project("test", staging=staging, url=url)

src = pyg.allocate_upload_directory(staging)
with open(os.path.join(src, "foo"), "w") as f:
    f.write("BAR")
os.mkdir(os.path.join(src, "whee"))
with open(os.path.join(src, "whee", "blah"), "w") as f:
    f.write("stuff")

pyg.upload_directory("test", "clone", "v1", src, staging=staging, url=url)


def test_clone_version():
    dest = tempfile.mkdtemp()
    out = pyg.clone_version("test", "clone", "v1", dest, registry=registry)

    fpath = os.path.join(dest, "foo")
    with open(fpath, "r") as handle:
        assert handle.read() == "BAR"
    assert os.path.exists(os.readlink(fpath))

    fpath = os.path.join(dest, "whee", "blah")
    with open(fpath, "r") as handle:
        assert handle.read() == "stuff"
    assert os.path.exists(os.readlink(fpath))
