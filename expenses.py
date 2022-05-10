import re
from typing import List, NamedTuple, Optional
import datetime
import pytz
from settings import path
import exceptions
from csv import writer, DictWriter


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str
    description: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    amount: int
    category_name: str


def add_expense(raw_message: str, user: int) -> Expense:
    """Добавляет расход.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)
#    print(parsed_message.amount)
#   print(parsed_message.category_text.upper())
    expence = [
        _get_now_formatted(),
        parsed_message.amount,
        parsed_message.category_text.upper(),
        parsed_message.description
    ]
    with open(_get_file_path(), mode="a") as file:
        writer(file).writerow(expence)
    return Expense(amount=parsed_message.amount, category_name=parsed_message.category_text)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _get_file_path() -> str:
    """Возвращает полный путь к файлу"""
    if len(path) > 1 and path[-1] == '/':
        full_file_name = path + "expenses.csv"
#        print(full_file_name)
    else:
        full_file_name = path + "/expenses.csv"
#        print(full_file_name)
    return full_file_name


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\-\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1500 метро")

    search_description = re.match(r"(.*)\.(.*)", regexp_result.group(2))

    amount = regexp_result.group(1).replace(" ", "")

    if not search_description or not search_description.group(0) \
            or not search_description.group(1) or not search_description.group(2):
        description = None
        category_text = regexp_result.group(2).strip().lower()
    else:
        description = search_description.group(2).strip().lower()
        category_text = search_description.group(1).strip().lower()

    return Message(amount=int(amount), category_text=category_text, description=description)
