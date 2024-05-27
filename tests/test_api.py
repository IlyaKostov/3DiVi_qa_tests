from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pytest

BASE_URL = "https://demo.3divi.ai/en/detect"


@pytest.fixture(scope="module")
def driver():
    """
    Инициализирует экземпляр WebDriver и переходит к установленному URL-адресу.
    Предоставляет драйвер для использования в тестах и завершает работу драйвера после завершения тестов.
    """
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    yield driver
    driver.quit()


def test_successful_detection(driver):
    """
    Проверяет успешное обнаружение человека на изображении.
    """
    upload_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload image')]")
    upload_button.click()

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_path = os.path.abspath("images/valid_image.jpg")
    file_input.send_keys(file_path)

    image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@class='chakra-image css-h4vxha']"))
    )

    detected_persons = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Detected persons')]/following-sibling::p"))
    )
    count_persons = detected_persons.text.split('/')

    assert image.is_displayed(), "Изображение не загрузилось"
    assert count_persons[1] == '1', "Ожидается, что обнаружен 1 человек"


def test_no_face_detection(driver):
    """
    Тестирует сценарий, в котором лица на изображении не обнаруживаются.
    """
    upload_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload image')]")
    upload_button.click()

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_path = os.path.abspath("images/no_face_image.jpg")
    file_input.send_keys(file_path)

    image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@class='chakra-image css-h4vxha']"))
    )

    faces = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "No faces found")]'))
    )

    assert image.is_displayed(), 'Изображение не загрузилось'
    assert faces.is_displayed(), 'Лица распознаны'


def test_invalid_file_upload(driver):
    """
    Тестирует загрузку файла недопустимого типа.
    """
    upload_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload image')]")
    upload_button.click()

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_path = os.path.abspath("images/invalid_file.txt")
    file_input.send_keys(file_path)

    wrong_file = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Only image can be uploaded")]'))
    )

    assert wrong_file.is_displayed()


def test_many_face_detection(driver):
    """
    Проверяет обнаружение нескольких лиц на изображении.
    """
    upload_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload image')]")
    upload_button.click()

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_path = os.path.abspath("images/many_face.jpg")
    file_input.send_keys(file_path)

    detected_persons = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Detected persons')]/following-sibling::p"))
    )
    count_persons = detected_persons.text.split('/')

    assert int(count_persons[1]) > 1, "Ожидается обнаружение более 1 лица"


def test_attributes_detection(driver):
    """
    Проверяет обнаружение таких атрибутов, как возраст и пол.
    """
    upload_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload image')]")
    upload_button.click()

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_path = os.path.abspath("images/valid_image.jpg")
    file_input.send_keys(file_path)

    age_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Age')]/following-sibling::p"))
    )

    gender_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Gender')]/following-sibling::p")

    assert "years" in age_element.text
    assert gender_element.text in ["Male", "Female"]


def test_high_size_image(driver):
    """
    Тестирует загрузку изображения, размер которого превышает максимально допустимый.
    """
    upload_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload image')]")
    upload_button.click()

    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_path = os.path.abspath("images/high_size_image.jpg")
    file_input.send_keys(file_path)

    high_size = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Image size must not exceed 4Mb.')]"))
    )

    assert high_size.is_displayed()


def test_take_a_photo(driver):
    """
    Проверка кнопки для создания фотографии
    """
    take_photo = driver.find_element(By.XPATH, "//button[contains(text(), 'Take a photo')]")
    take_photo.click()
    check_new_photo_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='chakra-button css-jvu0vq']"))
    )

    assert check_new_photo_button.is_displayed()
