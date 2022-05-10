"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import os
from settings import token, path, ACCESS_ID
from aiogram import Bot, Dispatcher, executor, types
import expenses
import exceptions
from middlewares import AccessMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)

"""Проверка клиента"""
dp.middleware.setup(AccessMiddleware(ACCESS_ID))

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для учёта финансов\n\n"
        "Добавить расход: 250 такси\n"
        "или 250 такси. в аэропорт"
        "Формат сообщения:\n"
        "Сумма Категория. Описание(не обязательно)\n")

@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новый расход"""
    try:
        expense = expenses.add_expense(message.text, message.from_user.id)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    answer_message = (f"Добавлены траты {expense.amount} руб на {expense.category_name}.")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
