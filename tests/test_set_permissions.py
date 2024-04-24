import pygobbler as pyg


def test_set_permissions():
    _, staging, registry, url = pyg.start_gobbler()
    pyg.remove_project("test-perms", staging=staging, url=url)
    pyg.create_project("test-perms", staging=staging, url=url, owners=["LTLA"])

    until = "2022-02-02T02:20:02.02Z"
    pyg.set_permissions("test-perms",
        owners=["jkanche"], 
        uploaders=[ { "id": "lawremi", "until": until } ],
        staging=staging,
        url=url,
        registry=registry
    )

    perms = pyg.fetch_permissions("test-perms", registry=registry, url=url)
    assert perms["owners"] == [ "LTLA", "jkanche" ]
    assert len(perms["uploaders"]) == 1
    assert perms["uploaders"][0]["id"] == "lawremi"
    assert perms["uploaders"][0]["until"] == until

    # Checking uploader appending, while also checking owners=NULL.
    pyg.set_permissions("test-perms", uploaders=[ { "id": "ArtifactDB-bot", "trusted": True } ], staging=staging, url=url, registry=registry)
    perms = pyg.fetch_permissions("test-perms", registry=registry, url=url)
    assert perms["owners"] == [ "LTLA", "jkanche" ]
    assert len(perms["uploaders"]) == 2
    assert perms["uploaders"][0]["id"] == "lawremi"
    assert perms["uploaders"][1]["id"] == "ArtifactDB-bot"
    assert perms["uploaders"][1]["trusted"]

    # Checking union of owners, and also that uploaders=NULL works.
    pyg.set_permissions("test-perms", owners=[ "PeteHaitch", "LTLA" ], staging=staging, url=url, registry=registry)
    perms = pyg.fetch_permissions("test-perms", registry=registry, url=url)
    assert perms["owners"] == [ "LTLA", "jkanche", "PeteHaitch" ]
    assert len(perms["uploaders"]) == 2

    # Resetting the owners back.
    pyg.set_permissions("test-perms", owners=[ "LTLA" ], append=False, staging=staging, url=url, registry=registry)
    perms = pyg.fetch_permissions("test-perms", registry=registry, url=url)
    assert perms["owners"] == [ "LTLA" ]
    assert len(perms["uploaders"]) == 2

    # Now resetting the uploaders. 
    pyg.set_permissions("test-perms", uploaders=[], append=False, staging=staging, url=url, registry=registry)
    perms = pyg.fetch_permissions("test-perms", registry=registry, url=url)
    assert perms["owners"] == [ "LTLA" ]
    assert len(perms["uploaders"]) == 0
