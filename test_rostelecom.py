from selenium.webdriver.common.by import By


def test_auth_form_is_displayed(driver):
    assert driver.find_element(By.XPATH, "//h1[contains(text(), 'Авторизация')]").is_displayed()


def test_phone_auth_is_selected_by_default(driver):
    phone_tab = driver.find_element(By.XPATH, "//div[contains(text(), 'Телефон')]")
    assert phone_tab.is_displayed()


def test_email_auth_tab_is_displayed(driver):
    email_tab = driver.find_element(By.XPATH, "//div[contains(text(), 'Почта')]")
    assert email_tab.is_displayed()


def test_login_auth_tab_is_displayed(driver):
    login_tab = driver.find_element(By.XPATH, "//div[contains(text(), 'Логин')]")
    assert login_tab.is_displayed()


def test_personal_account_tab_is_displayed(driver):
    account_tab = driver.find_element(By.XPATH, "//div[contains(text(), 'Лицевой счёт')]")
    assert account_tab.is_displayed()
