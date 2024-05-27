# Набор тестов 3DIVI API

Этот репозиторий содержит автоматизированные тесты для [3DIVI API](https://demo.3divi.ai/en/detect) с использованием `pytest` и `selenium`.  
Обращения к API происходят при загрузке изображения через web-интерфейс

## Настройка

1. Клонируйте репозиторий:
    ```sh
    git clone git@github.com:IlyaKostov/3DiVi_qa_tests.git
    ```

2. Запустите виртуальное окружение(в проекте используется poetry):
    ```sh
    poetry shell
    ```
   
3. Установите необходимые пакеты:
    ```sh
    poetry install
    ```

4. Скачайте и установите соответствующий WebDriver для вашего браузера (например, ChromeDriver для Google Chrome).  
Расположение ChromeDriver необходимо прописать в PATH.

## Запуск тестов

Для запуска тестов выполните следующую команду:
```sh
pytest
```

При выполнении последнего теста в браузере необходимо дать разрешение на подключение к камере. (фото выполняться не будет)




