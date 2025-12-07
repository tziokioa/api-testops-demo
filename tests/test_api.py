import pytest
import requests
import allure
from deepdiff import DeepDiff
import json


@allure.title("Compare API Responses")
def test_compare_endpoints(config):
    # 1. Setup URLs
    base_v1 = config['baseline'].rstrip('/')
    base_v2 = config['candidate'].rstrip('/')
    endpoint = config['endpoint']

    # Ensure leading slash
    if not endpoint.startswith('/'):
        endpoint = f"/{endpoint}"

    url_v1 = f"{base_v1}{endpoint}"
    url_v2 = f"{base_v2}{endpoint}"

    # 2. Execute Requests (No Headers needed for JSONPlaceholder)
    with allure.step(f"Fetch Baseline: {url_v1}"):
        resp_v1 = requests.get(url_v1)

    with allure.step(f"Fetch Candidate: {url_v2}"):
        resp_v2 = requests.get(url_v2)

    # 3. Check Status
    if resp_v1.status_code != 200:
        pytest.fail(f"Baseline failed! Status: {resp_v1.status_code}")
    if resp_v2.status_code != 200:
        pytest.fail(f"Candidate failed! Status: {resp_v2.status_code}")

    # 4. Compare JSON
    diff = DeepDiff(resp_v1.json(), resp_v2.json(), ignore_order=True)

    # 5. Report
    if diff:
        allure.attach(str(diff), name="Differences", attachment_type=allure.attachment_type.TEXT)
    else:
        allure.attach("Responses match perfectly.", name="Result", attachment_type=allure.attachment_type.TEXT)

    assert not diff, f"Regression found! {diff}"