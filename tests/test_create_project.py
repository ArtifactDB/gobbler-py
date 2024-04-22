import pygobbler as pyg
import datetime

_, staging, registry, url = pyg.start_gobbler()

def test_create_project():
    pyg.create_project(
        project="test-create",
        owners=["LTLA", "jkanche"],
        uploaders=[{ "id": "lawremi" }, { "id": "PeteHaitch", "until": datetime.datetime.utcnow().isoformat("T") + "Z" }],
        staging=staging,
        url=url
    )

    perms = pyg.fetch_permissions("test-create", registry, url=url)
    assert perms["owners"] == [ "LTLA", "jkanche" ]
    assert perms["uploaders"][0]["id"] == "lawremi"
    assert perms["uploaders"][1]["id"] == "PeteHaitch"
