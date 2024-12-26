# PS Store Deals Telegram Bot

## Description

This application is a Telegram bot that provides information about discounts on games on the PlayStation Store. The bot allows users to browse discounts by filtering them by a percentage threshold and get detailed information about the games, including the offer end date.

## How to launch

### Pre-requisites

1.  **Python 3.10 or later**: Make sure you have Python 3.10 or later installed. You can download the correct version from the [official Python website](https://www.python.org/downloads/).
2.  **Git:** (Optional) If you will be cloning a repository from GitHub, you will need Git.

### Installation

1.  **Clone the repository (or download the archive):**

    ```bash
    git clone https://github.com/UnWreckerNick/PSStoreDealsTG/
    cd <папка репозитория>
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```
3.  **Activate the virtual environment:**

    *   **Windows:**

        ```bash
        .\.venv\Scripts\activate
        ```
    *   **macOS/Linux:**

        ```bash
        source .venv/bin/activate
        ```
4.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    
5.  **Create file `.env`:**
     In the root directory of your project, create an `.env`.
6.  **Add the telegram bot token to the `.env`:**
    In the `.env` file, add the line::

    ```dotenv
    API_TOKEN=ВАШ_ТОКЕН_БОТА
    ```

    Replace `YOUR_BOT_TOKEN` token with the actual token of your Telegram bot. You can get the token by creating a bot from [@BotFather](https://t.me/botfather)  in Telegram.
    
8.  **Run the parser:**
    ```bash
    python <path to your parser file>/app/parser.py
    ```
    Replace  `<path to your parser file>/app/parser.py` with the path to your code file.
    
9.  **Run the bot after the parsing is complete:**
    ```bash
    python <path to your bot file>/app/app.py
    ```
    Replace `<path to your bot file>/app/app.py` with the path to your code file.

### How to use

After launching the bot in Telegram:

1. Enter the `/start` command to start the bot.
2. Enter the `/discounts` command to view the available discounts.
3. Select the discount level you are interested in (e.g. “50% and above”) or “Random Games”.
4. The bot will show a list of games with the appropriate discount, with the ability to navigate through the pages.
5. For each game, there are “Read More” and “Open in PSN Store” buttons.

### Dependencies

A list of all dependencies can be found in the `requirements.txt` file.

* `aiogram`: Library for creating Telegram bots.
* `beautifulsoup4`: Library for HTML and XML parsing.
* `requests`: Library for HTTP requests.
* `python-dotenv`: A library for `.env` files.

### Notes

*   This bot is intended for viewing discounts, it is not an official PlayStation application.
*   An internet connection is required for the bot to work.
*   Dates and end times of promotions may differ from actual values.
