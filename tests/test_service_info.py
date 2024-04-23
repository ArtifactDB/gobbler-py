import pygobbler as pyg

_, staging, registry, url = pyg.start_gobbler()


def test_service_info():
    payload = pyg.service_info(url)
    assert payload["staging"] == staging
    assert payload["registry"] == registry
