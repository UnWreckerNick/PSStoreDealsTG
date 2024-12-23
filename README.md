# PS Store Deals Telegram Bot

## Описание

Это приложение представляет собой Telegram-бота, который предоставляет информацию о скидках на игры в PlayStation Store. Бот позволяет пользователям просматривать скидки, фильтруя их по процентному порогу, и получать подробную информацию об играх, включая дату окончания предложения.

## Как запустить

### Предварительные требования

1.  **Python 3.10 или более поздняя версия:** Убедитесь, что у вас установлен Python 3.10 или более поздняя версия. Вы можете скачать нужную версию с [официального сайта Python](https://www.python.org/downloads/).
2.  **Git:** (Опционально) Если вы будете клонировать репозиторий с GitHub, вам понадобится Git.

### Установка

1.  **Клонируйте репозиторий (или скачайте архив):**

    ```bash
    git clone https://github.com/UnWreckerNick/PSStoreDealsTG/
    cd <папка репозитория>
    ```

2.  **Создайте виртуальное окружение:**

    ```bash
    python -m venv .venv
    ```
3.  **Активируйте виртуальное окружение:**

    *   **Windows:**

        ```bash
        .\.venv\Scripts\activate
        ```
    *   **macOS/Linux:**

        ```bash
        source .venv/bin/activate
        ```
4.  **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```
    Если файла `requirements.txt` нет, то нужно запустить следующую команду в папке проекта:
     ```bash
     pip install aiogram==2.25.2 beautifulsoup4 requests pipreqs
     pipreqs .
     ```
     и потом еще раз установить зависимсти.
5.  **Создайте файл `.env`:**
     В корневой директории вашего проекта создайте файл `.env`.
6.  **Добавьте токен телеграм-бота в `.env`:**
    В файле `.env` добавьте строку:

    ```dotenv
    API_TOKEN=ВАШ_ТОКЕН_БОТА
    ```

    Замените `ВАШ_ТОКЕН_БОТА` на фактический токен вашего Telegram-бота. Вы можете получить токен, создав бота у [@BotFather](https://t.me/botfather) в Telegram.
    
8.  **Запустите парсер:**
    ```bash
    python <путь к вашему файлу парсера>/app/parser.py
    ```
    Замените `<путь к вашему файлу бота>/app/parser.py` на путь до вашего файла с кодом.
    
9.  **Запустите бота после завершения парсинга:**
    ```bash
    python <путь к вашему файлу бота>/app/app.py
    ```
    Замените `<путь к вашему файлу бота>/app/app.py` на путь до вашего файла с кодом.

### Как использовать

После запуска бота в Telegram:

1.  Введите команду `/start`, чтобы начать работу с ботом.
2.  Введите команду `/discounts`, чтобы просмотреть доступные скидки.
3.  Выберите уровень скидки, который вас интересует (например, "50% и выше") или "Случайные игры".
4.  Бот покажет список игр с соответствующей скидкой, с возможностью навигации по страницам.
5.  Для каждой игры есть кнопки "Подробнее" и "Открыть в PSN Store".

### Зависимости

Список всех зависимостей находится в файле `requirements.txt`.

* `aiogram`: Библиотека для создания Telegram-ботов.
* `beautifulsoup4`: Библиотека для парсинга HTML и XML.
* `requests`: Библиотека для HTTP-запросов.
* `python-dotenv`: Библиотека для работы с файлами `.env`

### Примечания

*   Этот бот предназначен для просмотра скидок, он не является официальным приложением PlayStation.
*   Для работы бота необходимо подключение к Интернету.
*   Даты и время окончания акций могут отличаться от реальных значений.
