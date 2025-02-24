from playwright.sync_api import sync_playwright, expect
import config

def test_homepage_title():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/")

        title = page.title()

        assert title == "The Internet"

        browser.close()


def test_ab_testing_link():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/")

        test_ab_testing_link = page.locator("a[href= '/abtest']")
        test_ab_testing_link.click()

        expect(page).to_have_url("https://the-internet.herokuapp.com/abtest")

        browser.close()


def test_add_remove_elements():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/add_remove_elements/")
        add_button = page.locator("button", has_text="Add Element")
        add_button.click()
        delete_button = page.locator("button", has_text="Delete")

        expect(delete_button).to_be_visible()

        delete_button.click()

        expect(delete_button).to_be_hidden()
        browser.close()


from playwright.sync_api import sync_playwright, expect


# ... (оставляем предыдущие тесты без изменений)

def test_form_authentication_success():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/login")  # Переходим на страницу логина

        username_field = page.locator("#username")  # Находим поле "Username" по ID
        password_field = page.locator("#password")  # Находим поле "Password" по ID
        login_button = page.locator("button[type='submit']")  # Находим кнопку "Login" по типу "submit"

        username_field.fill("tomsmith")  # Вводим имя пользователя
        password_field.fill("SuperSecretPassword!")  # Вводим пароль
        login_button.click()  # Кликаем кнопку "Login"

        # Проверки после успешного логина:
        expect(page).to_have_url("https://the-internet.herokuapp.com/secure")  # Проверяем URL "Secure Area"
        success_message = page.locator(".flash.success")  # Находим сообщение об успехе по CSS-классу
        expect(success_message).to_be_visible()  # Проверяем, что сообщение об успехе видимо
        # Проверяем точный текст, как он есть
        expect(success_message).to_have_text("You logged into a secure area!\n×")

        browser.close()


# Login failure
def test_form_authentication_failure():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/login")

        username_field = page.locator("#username")  # Находим поле "Username" по ID
        password_field = page.locator("#password")  # Находим поле "Password" по ID
        login_button = page.locator("button[type='submit']")  # Находим кнопку "Login" по типу "submit"

        username_field.fill("wronguser")  # Вводим имя пользователя
        password_field.fill("wrongpassword")  # Вводим пароль
        login_button.click()  # Кликаем кнопку "Login"

        expect(page).to_have_url("https://the-internet.herokuapp.com/login")
        error_message = page.locator(".flash.error")
        expect(error_message).to_be_visible()
        # Проверяем точный текст, как он есть
        expect(error_message).to_have_text("Your username is invalid!\n×")

        browser.close()


# Checkboxes
def test_checkboxes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/checkboxes")

        checkbox1 = page.locator("input[type='checkbox']").nth(0)
        checkbox2 = page.locator("input[type='checkbox']").nth(1)

        expect(checkbox1).not_to_be_checked()
        expect(checkbox2).to_be_checked()

        checkbox1.check()  # Выключаем первый
        checkbox2.uncheck()

        expect(checkbox1).to_be_checked()
        expect(checkbox2).not_to_be_checked()

        browser.close()


# Dynamic loading
def test_dynamic_loading():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")

        start_button = page.locator("button")
        start_button.click()

        finish_message = page.locator("#finish")
        expect(finish_message).to_be_visible(timeout=10000)
        expect(finish_message).to_have_text("Hello World!")

        browser.close()





