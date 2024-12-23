import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
import json
from config import API_TOKEN


def load_games_data(filename="psn_deals_full.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


games_data = load_games_data()


def get_discount_value(game):
    discount = game.get("discount_percent", "N/A")
    if discount == "N/A":
        return 0
    try:
        return int(discount.strip('%').strip('-'))
    except ValueError:
        return 0


def filter_games(discount_threshold):
    filtered_games = []

    for game in games_data:
        if discount_threshold == 0:
            filtered_games.append(game)
            continue

        discount = game.get("discount_percent", "N/A")
        if discount == "N/A":
            continue

        try:
            discount_value = int(discount.strip('%').strip('-'))
            if discount_value >= discount_threshold:
                filtered_games.append(game)
        except ValueError:
            print(
                f"Skipping game with invalid discount_percent: {game.get('name', 'N/A')}, Value: {discount}")
            continue

    if discount_threshold > 0:
        filtered_games.sort(
            key=get_discount_value,
            reverse=True
        )

    return filtered_games


def create_game_keyboard(game):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подробнее", callback_data=f"details_{game['url']}")],
        [InlineKeyboardButton(text="Открыть в PSN Store", url=f"https://store.playstation.com{game['url']}")]
    ])
    return keyboard


async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот с PSN скидками. Используй /discounts для просмотра скидок.")


async def discounts_handler(message: types.Message):
    await message.answer(
        "Выберите опцию:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="50% и выше", callback_data="filter_50_0")],
            [InlineKeyboardButton(text="75% и выше", callback_data="filter_75_0")],
            [InlineKeyboardButton(text="Все скидки", callback_data="filter_0_0")],
            [InlineKeyboardButton(text="🎲 Случайные игры", callback_data="random_games")]
        ])
    )


async def filter_callback(callback: types.CallbackQuery):
    data_parts = callback.data.split("_")
    threshold = int(data_parts[1])
    page = int(data_parts[2])
    filtered_games = filter_games(threshold)
    items_per_page = 10
    start_index = page * items_per_page
    end_index = start_index + items_per_page

    if not filtered_games:
        await callback.message.answer(f"Нет игр с уровнем скидки {threshold}% и выше.")
        return

    for game in filtered_games[start_index:end_index]:
        if game.get("discount_percent", "N/A") == "N/A":
            text = (
                f"🎮 <b>{game['name']}</b>\n"
                f"💰 Оригинальная цена: {game['base_price']}"
            )
        else:
            text = (
                f"🎮 <b>{game['name']}</b>\n"
                f"💰 Скидка: {game['discount_percent']}\n"
                f"Цена со скидкой: {game['discount_price']}\n"
                f"Оригинальная цена: {game['base_price']}"
            )
        await callback.message.answer(
            text,
            reply_markup=create_game_keyboard(game),
            parse_mode="HTML"
        )

    total_pages = (len(filtered_games) + items_per_page - 1) // items_per_page
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    if page > 0:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="< Предыдущая", callback_data=f"filter_{threshold}_{page - 1}")])
    if page < total_pages - 1:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="Следующая >", callback_data=f"filter_{threshold}_{page + 1}")])

    if keyboard.inline_keyboard:
        await callback.message.answer("Страницы:", reply_markup=keyboard)


async def details_callback(callback: types.CallbackQuery):
    game_url = callback.data.split("_", 1)[1]
    game = next((g for g in games_data if g["url"] == game_url), None)

    if not game:
        await callback.message.answer("Ошибка: игра не найдена.")
        return

    text = (
        f"🎮 <b>{game['name']}</b>\n"
        f"💰 Скидка: {game['discount_percent']}\n"
        f"Цена со скидкой: {game['discount_price']}\n"
        f"Оригинальная цена: {game['base_price']}\n"
        f"📅 Срок действия: {game['offer_end_date']}\n"
        f"🔗 [Открыть в PSN Store](https://store.playstation.com{game['url']})"
    )
    await callback.message.answer(text, parse_mode="HTML")


async def random_games_callback(callback: types.CallbackQuery):
    games_with_discounts = [game for game in games_data if game.get("discount_percent", "N/A") != "N/A"]

    if not games_with_discounts:
        await callback.message.answer("К сожалению, сейчас нет игр со скидками.")
        return

    num_games = min(10, len(games_with_discounts))
    random_selection = random.sample(games_with_discounts, num_games)

    await callback.message.answer("🎲 Вот случайная подборка игр со скидками:")

    for game in random_selection:
        text = (
            f"🎮 <b>{game['name']}</b>\n"
            f"💰 Скидка: {game['discount_percent']}\n"
            f"Цена со скидкой: {game['discount_price']}\n"
            f"Оригинальная цена: {game['base_price']}"
        )
        await callback.message.answer(
            text,
            reply_markup=create_game_keyboard(game),
            parse_mode="HTML"
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🎲 Показать другие случайные игры", callback_data="random_games")
    ]])
    await callback.message.answer("Хотите посмотреть другие случайные игры?", reply_markup=keyboard)


async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, Command(commands=["start"]))
    dp.message.register(discounts_handler, Command(commands=["discounts"]))
    dp.callback_query.register(filter_callback, lambda cb: cb.data.startswith("filter_"))
    dp.callback_query.register(details_callback, lambda cb: cb.data.startswith("details_"))
    dp.callback_query.register(random_games_callback, lambda cb: cb.data == "random_games")

    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="discounts", description="Посмотреть скидки")
    ])

    try:
        print("Бот запущен...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())