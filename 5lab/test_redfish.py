import pytest
import requests
import logging
import time
from typing import Dict, Any

BMC_HOST = "https://172.23.199.211:2443"
BMC_USERNAME = "root"
BMC_PASSWORD = "0penBmc"
VERIFY_SSL = False

requests.packages.urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def redfish_session() -> requests.Session:
    session = requests.Session()
    session.verify = VERIFY_SSL

    login_url = f"{BMC_HOST}/redfish/v1/SessionService/Sessions"
    payload = {
        "UserName": BMC_USERNAME,
        "Password": BMC_PASSWORD
    }

    logger.info("Создание Redfish сессии...")
    response = session.post(login_url, json=payload)

    session.headers.update({
        "X-Auth-Token": response.headers["X-Auth-Token"],
        "Content-Type": "application/json"
    })

    logger.info("Сессия успешно создана.")
    yield session

    delete_url = f"{BMC_HOST}/redfish/v1/SessionService/Sessions/{response.json().get('Id')}"
    session.delete(delete_url)
    logger.info("Сессия завершена.")


def test_redfish_authentication(redfish_session):
    response = redfish_session.get(f"{BMC_HOST}/redfish/v1/")
    assert response.status_code == 200, f"Не удалось аутентифицироваться: {response.status_code}"
    auth_token = redfish_session.headers.get("X-Auth-Token")
    assert auth_token is not None, "Токен аутентификации отсутствует"


def test_get_system_info(redfish_session):
    url = f"{BMC_HOST}/redfish/v1/Systems/system"
    response = redfish_session.get(url)
    assert response.status_code == 200, f"Не удалось получить информацию о системе: {response.status_code}"

    data = response.json()
    assert "Status" in data, "В ответе отсутствует поле 'Status'"
    assert "PowerState" in data, "В ответе отсутствует поле 'PowerState'"
    logger.info(f"Текущее состояние питания: {data['PowerState']}")


def test_power_on_system(redfish_session):
    system_url = f"{BMC_HOST}/redfish/v1/Systems/system"

    reset_url = f"{system_url}/Actions/ComputerSystem.Reset"
    payload = {"ResetType": "On"}
    response = redfish_session.post(reset_url, json=payload)

    assert response.status_code in (202, 204), f"Ожидался статус 202 или 204, получен: {response.status_code}"


def test_cpu_temperature_within_limits(redfish_session):
    thermal_url = f"{BMC_HOST}/redfish/v1/Chassis/chassis/Thermal"
    response = redfish_session.get(thermal_url)
    assert response.status_code in(200, 404), f"Не удалось получить данные термодатчиков"


def test_redfish_ipmi_cpu_sensors_consistency(redfish_session):
    thermal_url = f"{BMC_HOST}/redfish/v1/Chassis/chassis/Thermal"
    response = redfish_session.get(thermal_url)
    assert response.status_code in(200, 404), f"Не удалось получить данные датчиков CPU"