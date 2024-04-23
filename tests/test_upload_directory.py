import pygobbler as pyg
import tempfile
import os

_, staging, registry, url = pyg.start_gobbler()
pyg.remove_project("test-upload", staging=staging, url=url)
pyg.remove_project("test-more-upload", staging=staging, url=url)
pyg.remove_project("test-upload-perms", staging=staging, url=url)
pyg.create_project("test-upload", staging=staging, url=url)
pyg.create_project("test-more-upload", staging=staging, url=url)
pyg.create_project("test-upload-perms", staging=staging, url=url)

tmp = tempfile.mkdtemp()
with open(os.path.join(tmp, "blah.txt"), "w") as f:
    f.write("BAR")
os.mkdir(os.path.join(tmp, "foo"))
with open(os.path.join(tmp, "foo", "bar.txt"), "w") as f:
    f.write("1 2 3 4 5 6 7 8 9 10")


def test_upload_directory_simple():
    pyg.upload_directory(
        project="test-upload", 
        asset="jennifer", 
        version="1", 
        directory=tmp,
        staging=staging, 
        url=url
    )

    # Checking that the files were, in fact, correctly uploaded.
    man = pyg.fetch_manifest("test-upload", "jennifer", "1", registry=registry, url=url)
    assert sorted(man.keys()) == ["blah.txt", "foo/bar.txt"]
    for k, v in man.items():
        assert "link" not in v

    # Deduplication happens naturally.
    pyg.upload_directory(
        project="test-upload", 
        asset="jennifer", 
        version="2", 
        directory=tmp,
        staging=staging,
        url=url
    )

    man = pyg.fetch_manifest("test-upload", "jennifer", "2", registry=registry, url=url)
    assert sorted(man.keys()) == ["blah.txt", "foo/bar.txt"]
    for k, v in man.items():
        assert "link" in v


def test_upload_directory_links():
    dest = tempfile.mkdtemp()
    pyg.clone_version("test-upload", "jennifer", "2", dest, registry=registry)
    with open(os.path.join(dest, "whee"), "w") as f:
        f.write("BLAH")

    pyg.upload_directory(
        project="test-more-upload", 
        asset="natalie", 
        version="1", 
        directory=dest,
        staging=staging,
        url=url
    )

    man = pyg.fetch_manifest("test-more-upload", "natalie", "1", registry=registry, url=url)
    assert sorted(man.keys()) == ["blah.txt", "foo/bar.txt", "whee"]
    assert "link" in man["blah.txt"]
    assert "link" in man["foo/bar.txt"]
    assert "link" not in man["whee"]


def test_upload_directory_staging():
    dir = pyg.allocate_upload_directory(staging)
    with open(os.path.join(dir, "blah.txt"), "w") as f:
        f.write("A B C D E")
    os.mkdir(os.path.join(dir, "foo"))
    with open(os.path.join(dir, "foo", "bar.txt"), "w") as f:
        f.write("1 2 3 4 5 6 7 8 9 10")

    pyg.upload_directory(
        project="test-upload", 
        asset="jennifer", 
        version="3", 
        directory=dir,
        staging=staging,
        url=url
    )

    man  = pyg.fetch_manifest("test-upload", "jennifer", "3", registry=registry, url=url)
    assert sorted(man.keys()) == ["blah.txt", "foo/bar.txt"]
    assert "link" not in man["blah.txt"]
    assert "link" in man["foo/bar.txt"]
