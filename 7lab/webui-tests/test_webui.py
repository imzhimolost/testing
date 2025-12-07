import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


LOGIN_URL = "https://localhost:2443/#/login"

VALID_USERNAME = "root"
VALID_PASSWORD = "0penBmc"
INVALID_PASSWORD = "No0penBmc"

VALID_TEST_USERNAME = "test_user"
VALID_TEST_PASSWORD = "TestPass123"
INVALID_TEST_PASSWORD = "111111111"

def login(driver, username, password, force_reload=True):
    if force_reload:
        driver.get(LOGIN_URL)

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form.login-form"))
    )

    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.clear()
    password_field.clear()

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()

def test_successful_login(driver):
    login(driver, VALID_USERNAME, VALID_PASSWORD)

    user_label = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'root')]"))
    )
    assert user_label.is_displayed(), "Имя пользователя 'root' не отображается"

    assert driver.current_url.endswith("/"), f"Ожидался URL с /, получено: {driver.current_url}"

def test_invalid_credentials(driver):
    login(driver, VALID_USERNAME, INVALID_PASSWORD)

    assert "/login" in driver.current_url or "login" in driver.current_url.lower(), \
        f"Ожидалась страница входа, но URL: {driver.current_url}"

def test_account_lockout(driver):
    driver.get(LOGIN_URL)

    for _ in range(3):
        login(driver, VALID_TEST_USERNAME, INVALID_TEST_PASSWORD, force_reload=False)

        login_form = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form.login-form"))
        )
        assert login_form.is_displayed(), "Форма входа не найдена"

        time.sleep(5)

    login(driver, VALID_TEST_USERNAME, VALID_TEST_PASSWORD, force_reload=False)

    assert "/login" in driver.current_url or "login" in driver.current_url.lower(), \
        f"Ожидалась страница входа, но URL: {driver.current_url}"

def test_power_off(driver):
    login(driver, VALID_USERNAME, VALID_PASSWORD)

def test_temperature(driver):
    login(driver, VALID_USERNAME, VALID_PASSWORD)