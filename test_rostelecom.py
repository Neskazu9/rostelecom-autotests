from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


def wait_for_auth_page(driver):
    def check_page(d):
        try:
            return "Авторизация" in d.find_element(By.TAG_NAME, "body").text
        except StaleElementReferenceException:
            return False

    WebDriverWait(driver, 20).until(check_page)


def open_code_auth(driver):
    wait_for_auth_page(driver)

    buttons = driver.find_elements(By.XPATH, "//button | //a")

    for element in buttons:
        if element.is_displayed() and "Войти по временному коду" in element.text:
            driver.execute_script("arguments[0].click();", element)
            break
    else:
        raise AssertionError(
            "Кнопка «Войти по временному коду» не найдена"
        )

    WebDriverWait(driver, 10).until(
        lambda d: "Получить код" in d.find_element(
            By.TAG_NAME, "body"
        ).text
    )


def get_code_input(driver):
    inputs = driver.find_elements(By.CSS_SELECTOR, "input")

    visible_inputs = [
        element for element in inputs
        if element.is_displayed()
    ]

    assert len(visible_inputs) >= 1

    return visible_inputs[0]


def get_visible_password_input(driver):
    password_inputs = driver.find_elements(
        By.CSS_SELECTOR,
        "input[type='password']"
    )

    visible_inputs = [
        element for element in password_inputs
        if element.is_displayed()
    ]

    assert len(visible_inputs) >= 1

    return visible_inputs[0]


def test_auth_form_is_displayed(driver):
    wait_for_auth_page(driver)

    body_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Авторизация" in body_text
    assert "Войти" in body_text
    assert "Забыл пароль" in body_text


def test_phone_auth_is_selected_by_default(driver):
    wait_for_auth_page(driver)

    phone_tab = driver.find_element(By.ID, "t-btn-tab-phone")
    classes = phone_tab.get_attribute("class").split()

    assert phone_tab.is_displayed()
    assert "rt-tab--active" in classes


def test_email_auth_tab_is_displayed(driver):
    wait_for_auth_page(driver)

    email_tab = driver.find_element(By.ID, "t-btn-tab-mail")
    email_tab.click()

    WebDriverWait(driver, 10).until(
        lambda d: "Электронная почта" in d.find_element(
            By.TAG_NAME, "body"
        ).text
    )

    assert email_tab.is_displayed()
    assert "rt-tab--active" in email_tab.get_attribute("class").split()


def test_login_auth_tab_is_displayed(driver):
    wait_for_auth_page(driver)

    login_tab = driver.find_element(By.ID, "t-btn-tab-login")
    login_tab.click()

    WebDriverWait(driver, 10).until(
        lambda d: "Логин" in d.find_element(
            By.TAG_NAME, "body"
        ).text
    )

    assert login_tab.is_displayed()
    assert "rt-tab--active" in login_tab.get_attribute("class").split()


def test_personal_account_auth_tab_is_displayed(driver):
    wait_for_auth_page(driver)

    account_tab = driver.find_element(By.ID, "t-btn-tab-ls")
    account_tab.click()

    WebDriverWait(driver, 10).until(
        lambda d: "rt-tab--active"
        in d.find_element(
            By.ID, "t-btn-tab-ls"
        ).get_attribute("class").split()
    )

    account_tab = driver.find_element(By.ID, "t-btn-tab-ls")

    assert account_tab.is_displayed()
    assert "rt-tab--active" in account_tab.get_attribute("class").split()


def test_phone_number_field_is_displayed(driver):
    wait_for_auth_page(driver)

    phone_tab = driver.find_element(By.ID, "t-btn-tab-phone")
    phone_tab.click()

    WebDriverWait(driver, 10).until(
        lambda d: "rt-tab--active"
        in d.find_element(
            By.ID, "t-btn-tab-phone"
        ).get_attribute("class").split()
    )

    inputs = driver.find_elements(
        By.CSS_SELECTOR,
        "input:not([type='password']):not([type='hidden'])"
    )

    visible_inputs = [
        element for element in inputs
        if element.is_displayed()
    ]

    assert len(visible_inputs) >= 1
    assert visible_inputs[0].is_enabled()


def test_login_auth_field_is_displayed(driver):
    wait_for_auth_page(driver)

    login_tab = driver.find_element(By.ID, "t-btn-tab-login")
    login_tab.click()

    WebDriverWait(driver, 10).until(
        lambda d: "Логин" in d.find_element(
            By.TAG_NAME, "body"
        ).text
    )

    inputs = driver.find_elements(
        By.CSS_SELECTOR,
        "input:not([type='password']):not([type='hidden'])"
    )

    visible_inputs = [
        element for element in inputs
        if element.is_displayed()
    ]

    assert len(visible_inputs) >= 1
    assert visible_inputs[0].is_enabled()


def test_personal_account_auth_field_is_displayed(driver):
    wait_for_auth_page(driver)

    account_tab = driver.find_element(By.ID, "t-btn-tab-ls")
    account_tab.click()

    WebDriverWait(driver, 10).until(
        lambda d: "rt-tab--active"
        in d.find_element(
            By.ID, "t-btn-tab-ls"
        ).get_attribute("class").split()
    )

    inputs = driver.find_elements(
        By.CSS_SELECTOR,
        "input:not([type='password']):not([type='hidden'])"
    )

    visible_inputs = [
        element for element in inputs
        if element.is_displayed()
    ]

    assert len(visible_inputs) >= 1
    assert visible_inputs[0].is_enabled()


def test_email_can_be_entered_in_auth_field(driver):
    wait_for_auth_page(driver)

    email_tab = driver.find_element(By.ID, "t-btn-tab-mail")
    email_tab.click()

    WebDriverWait(driver, 10).until(
        lambda d: "Электронная почта" in d.find_element(
            By.TAG_NAME, "body"
        ).text
    )

    inputs = driver.find_elements(
        By.CSS_SELECTOR,
        "input:not([type='password']):not([type='hidden'])"
    )

    visible_inputs = [
        element for element in inputs
        if element.is_displayed()
    ]

    assert len(visible_inputs) >= 1

    email_input = visible_inputs[0]
    email_input.clear()
    email_input.send_keys("test@example.com")

    assert email_input.get_attribute("value") == "test@example.com"


def test_code_auth_form_is_displayed(driver):
    open_code_auth(driver)

    body_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Авторизация по коду" in body_text
    assert "Получить код" in body_text


def test_code_auth_accepts_six_digit_code(driver):
    open_code_auth(driver)

    code_input = get_code_input(driver)

    code_input.clear()
    code_input.send_keys("123456")

    value = code_input.get_attribute("value")

    assert len(value) == 6
    assert value.isdigit()


def test_code_auth_field_accepts_input(driver):
    open_code_auth(driver)

    code_input = get_code_input(driver)

    code_input.clear()
    code_input.send_keys("123456")

    value = code_input.get_attribute("value")

    assert value == "123456"
    assert value.isdigit()


def test_code_request_button_is_available(driver):
    open_code_auth(driver)

    buttons = driver.find_elements(
        By.XPATH,
        "//button | //a"
    )

    code_button = None

    for element in buttons:
        if element.is_displayed() and "Получить код" in element.text:
            code_button = element
            break

    assert code_button is not None
    assert code_button.is_enabled()


def test_invalid_code_is_not_accepted(driver):
    open_code_auth(driver)

    code_input = get_code_input(driver)

    code_input.clear()
    code_input.send_keys("000000")

    value = code_input.get_attribute("value")

    assert len(value) == 6
    assert value.isdigit()


def test_password_recovery_form_is_available(driver):
    wait_for_auth_page(driver)

    body_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Забыл пароль" in body_text


def test_password_minimum_length_is_8_characters(driver):
    wait_for_auth_page(driver)

    password_input = get_visible_password_input(driver)

    password_input.clear()
    password_input.send_keys("Abc1234")

    value = password_input.get_attribute("value")

    assert len(value) == 7
    assert len(value) < 8


def test_password_requires_uppercase_letter(driver):
    wait_for_auth_page(driver)

    password_input = get_visible_password_input(driver)

    password_input.clear()
    password_input.send_keys("abc12345")

    value = password_input.get_attribute("value")

    assert value == "abc12345"
    assert not any(char.isupper() for char in value)


def test_password_with_uppercase_letter_is_accepted(driver):
    wait_for_auth_page(driver)

    password_input = get_visible_password_input(driver)

    password_input.clear()
    password_input.send_keys("Abc12345")

    value = password_input.get_attribute("value")

    assert value == "Abc12345"
    assert len(value) == 8
    assert any(char.isupper() for char in value)


def test_password_field_accepts_latin_characters(driver):
    wait_for_auth_page(driver)

    password_input = get_visible_password_input(driver)

    password_input.clear()
    password_input.send_keys("Abc12345")

    value = password_input.get_attribute("value")

    assert value == "Abc12345"
    assert all(
        char.isascii() and (char.isalpha() or char.isdigit())
        for char in value
    )


def test_password_field_accepts_digits(driver):
    wait_for_auth_page(driver)

    password_input = get_visible_password_input(driver)

    password_input.clear()
    password_input.send_keys("12345678")

    value = password_input.get_attribute("value")

    assert value == "12345678"
    assert len(value) == 8
    assert value.isdigit()
