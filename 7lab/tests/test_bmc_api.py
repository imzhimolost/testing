import requests
import pytest

BASE_URL = "https://localhost:2443"
AUTH = ("root", "0penBmc")

requests.packages.urllib3.disable_warnings()

def test_redfish_root():
    r = requests.get(f"{BASE_URL}/redfish/v1", auth=AUTH, verify=False)
    assert r.status_code == 200
    data = r.json()
    assert "RedfishVersion" in data

def test_bmc_version():
    r = requests.get(f"{BASE_URL}/redfish/v1/Managers/bmc", auth=AUTH, verify=False)
    assert r.status_code == 200
    data = r.json()
    assert "Model" in data
    print(f"Model: {data['Model']}")

def test_power_status():
    r = requests.get(f"{BASE_URL}/redfish/v1/Systems/system", auth=AUTH, verify=False)
    assert r.status_code == 200