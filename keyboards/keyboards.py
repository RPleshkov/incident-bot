from datetime import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def add_incident() -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(
        text="Зафиксировать инцидент", callback_data="add_incident"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


def current_time_kb(current_time) -> InlineKeyboardMarkup:
    
    button = InlineKeyboardButton(text=current_time, callback_data="current_time_btn")
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


def confirm_or_refill() -> InlineKeyboardMarkup:
    button1 = InlineKeyboardButton(
        text="Подтвердить ✅", callback_data="confirm_pressed"
    )
    button2 = InlineKeyboardButton(
        text="Заполнить заново ❌", callback_data="refil_pressed"
    )
    return InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])


def sti_res_kb() -> InlineKeyboardMarkup:
    button1 = InlineKeyboardButton(text="Да ✅", callback_data="sti_yes")
    button2 = InlineKeyboardButton(text="Нет ❌", callback_data="sti_no")
    return InlineKeyboardMarkup(inline_keyboard=[[button1, button2]])


def admin_menu() -> InlineKeyboardMarkup:
    button1 = InlineKeyboardButton(text="Выгрузить Excel", callback_data="get_excel")
    button2 = InlineKeyboardButton(text="Выйти", callback_data="quit")
    return InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])
