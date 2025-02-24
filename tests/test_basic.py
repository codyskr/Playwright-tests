from playwright.sync_api import sync_playwright, expect
#import pytest
import config
import os

# Тест-кейс 1: Проверка заголовка главной страницы

def test_homepage_title():
    # Запускаем Playwright в синхронном режиме с настройкой UI из config
    with sync_playwright() as p:
        # Открываем браузер — headless или с UI, зависит от config.HEADLESS
        browser = p.chromium.launch(headless=config.HEADLESS)
        # Создаём новую страницу для теста
        page = browser.new_page()
        # Переходим на главную страницу сайта — Playwright сам подождёт загрузки
        page.goto("https://the-internet.herokuapp.com/")

        # Берем заголовок страницы и проверяем, что он соответствует ожидаемому
        title = page.title()
        assert title == "The Internet", "Заголовок главной страницы не совпадает с ожидаемым"

        # Закрываем браузер — всё чисто и аккуратно
        browser.close()

# Тест-кейс 2: Проверка перехода по ссылке A/B Testing
def test_ab_testing_link():
    # Запускаем Playwright и открываем браузер с настройками из config
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        # Загружаем главную страницу сайта
        page.goto("https://the-internet.herokuapp.com/")

        # Находим ссылку по атрибуту href и кликаем — Playwright подождёт, пока она станет доступной
        test_ab_testing_link = page.locator("a[href='/abtest']")
        test_ab_testing_link.click()

        # Проверяем, что после клика нас перенаправило на нужный URL
        expect(page).to_have_url("https://the-internet.herokuapp.com/abtest"), "URL после клика не совпадает"

        # Закрываем всё, чтобы не оставлять "мусора"
        browser.close()

# Тест-кейс 3: Добавление и удаление элементов

def test_add_remove_elements():
    # Запускаем Playwright, открываем браузер с учётом настройки UI
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        # Переходим на страницу с добавлением/удалением элементов
        page.goto("https://the-internet.herokuapp.com/add_remove_elements/")

        # Находим кнопку "Add Element" и кликаем — добавляем новый элемент
        add_button = page.locator("button", has_text="Add Element")
        add_button.click()

        # Теперь ищем кнопку "Delete", которая появилась после добавления
        delete_button = page.locator("button", has_text="Delete")
        # Проверяем, что кнопка видна — значит, элемент добавлен
        expect(delete_button).to_be_visible(), "Кнопка Delete не отображается после добавления"

        # Кликаем "Delete" для удаления элемента
        delete_button.click()

        # Убеждаемся, что кнопка исчезла — элемент удалён
        expect(delete_button).to_be_hidden(), "Кнопка Delete осталась видимой после удаления"

        # Завершаем тест, закрывая браузер
        browser.close()

# Тест-кейс 4: Успешный логин на странице

def test_form_authentication_success():
    # Запускаем Playwright и открываем браузер с настройкой UI
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        # Переходим на страницу логина — ждём полной загрузки
        page.goto("https://the-internet.herokuapp.com/login")  # Переходим на страницу логина

        # Находим поля ввода и кнопку логина по ID и атрибутам
        username_field = page.locator("#username")  # Поле для имени пользователя
        password_field = page.locator("#password")  # Поле для пароля
        login_button = page.locator("button[type='submit']")  # Кнопка входа

        # Вводим корректные данные для успешного логина
        username_field.fill("tomsmith")  # Вводим имя пользователя
        password_field.fill("SuperSecretPassword!")  # Вводим пароль
        login_button.click()  # Кликаем кнопку "Login"

        # Проверяем, что нас перенаправило на защищённую область
        expect(page).to_have_url("https://the-internet.herokuapp.com/secure"), "URL после логина не совпадает"
        # Находим сообщение об успехе и проверяем его видимость и текст
        success_message = page.locator(".flash.success")  # Сообщение об успехе
        expect(success_message).to_be_visible(), "Сообщение об успехе не отображается"
        # Убеждаемся, что текст сообщения точно такой, как на странице, включая перенос строки и крестик
        expect(success_message).to_have_text("You logged into a secure area!\n×"), "Текст сообщения об успехе не совпадает"

        # Завершаем, закрывая браузер
        browser.close()

# Тест-кейс 5: Неудачный логин на странице

def test_form_authentication_failure():
    # Запускаем Playwright с настройкой UI из config
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        # Переходим на страницу логина
        page.goto("https://the-internet.herokuapp.com/login")

        # Находим поля ввода и кнопку логина
        username_field = page.locator("#username")  # Поле для имени пользователя
        password_field = page.locator("#password")  # Поле для пароля
        login_button = page.locator("button[type='submit']")  # Кнопка входа

        # Вводим неверные данные для провала логина
        username_field.fill("wronguser")  # Вводим неверное имя пользователя
        password_field.fill("wrongpassword")  # Вводим неверный пароль
        login_button.click()  # Пытаемся войти

        # Проверяем, что URL остался прежним — логин не удался
        expect(page).to_have_url("https://the-internet.herokuapp.com/login"), "URL изменился, хотя логин должен был провалиться"
        # Находим сообщение об ошибке и проверяем его
        error_message = page.locator(".flash.error")  # Сообщение об ошибке
        expect(error_message).to_be_visible(), "Сообщение об ошибке не отображается"
        # Убеждаемся, что текст ошибки точно такой, как ожидается, с переносом и крестиком
        expect(error_message).to_have_text("Your username is invalid!\n×"), "Текст сообщения об ошибке не совпадает"

        # Завершаем тест, закрывая браузер
        browser.close()

# Тест-кейс 6: Работа с чекбоксами

def test_checkboxes():
    # Запускаем Playwright с настройкой UI
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        # Переходим на страницу с чекбоксами
        page.goto("https://the-internet.herokuapp.com/checkboxes")

        # Находим два чекбокса на странице — первый и второй
        checkbox1 = page.locator("input[type='checkbox']").nth(0)  # Первый чекбокс
        checkbox2 = page.locator("input[type='checkbox']").nth(1)  # Второй чекбокс

        # Проверяем начальное состояние — на сайте первый выключен, второй включён (по умолчанию)
        expect(checkbox1).not_to_be_checked(), "Первый чекбокс должен быть выключен изначально"
        expect(checkbox2).to_be_checked(), "Второй чекбокс должен быть включён изначально"

        # Изменяем состояние: включаем первый, выключаем второй
        checkbox1.check()  # Ставим галочку на первом
        checkbox2.uncheck()  # Снимаем галочку со второго

        # Проверяем, что состояния изменились
        expect(checkbox1).to_be_checked(), "Первый чекбокс не включён после изменения"
        expect(checkbox2).not_to_be_checked(), "Второй чекбокс не выключен после изменения"

        # Закрываем браузер, завершяя тест
        browser.close()

# Тест-кейс 7: Проверка динамической загрузки

def test_dynamic_loading():
    # Запускаем Playwright с настройкой UI
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        # Переходим на страницу с динамической загрузкой (вариант 2)
        page.goto("https://the-internet.herokuapp.com/dynamic_loading/2")

        # Находим и кликаем на кнопку "Start", чтобы запустить загрузку
        start_button = page.locator("button")
        start_button.click()

        # Находим элемент, который появится после загрузки, и ждём до 10 секунд
        finish_message = page.locator("#finish")
        expect(finish_message).to_be_visible(timeout=10000), "Элемент не стал видимым после загрузки"
        # Проверяем, что текст элемента соответствует ожидаемому
        expect(finish_message).to_have_text("Hello World!"), "Текст после загрузки не совпадает"

        # Завершаем тест, закрывая браузер
        browser.close()

# Тест-кейс 8: Скачивание файла

def test_file_download():
    # Запускаем Playwright с настройкой UI
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.HEADLESS)
        page = browser.new_page()
        # Переходим на страницу скачивания файлов
        page.goto("https://the-internet.herokuapp.com/download")

        # Находим первую ссылку на .txt файл и кликаем, ожидая скачивания
        download_link = page.locator("a[href*='.txt']").first
        with page.expect_download() as download_info:
            download_link.click()

        # Получаем информацию о скачанном файле
        download = download_info.value
        file_name = download.suggested_filename
        # Проверяем, что имя файла заканчивается на .txt
        assert file_name.endswith(".txt"), f"Ожидался файл .txt, получено: {file_name}"

        # Сохраняем файл в текущую директорию и проверяем, что он существует
        download_path = os.path.join(os.getcwd(), file_name)
        download.save_as(download_path)
        assert os.path.exists(download_path), f"Файл {download_path} не был сохранён"

        # Завершаем тест, закрывая браузер
        browser.close()