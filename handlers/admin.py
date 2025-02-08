from datetime import date, datetime
import logging
import os
from aiogram.types import CallbackQuery, FSInputFile
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Back, Button, Calendar, Next
from aiogram_dialog.widgets.text import Const, Format, Multi
from sqlalchemy.ext.asyncio import AsyncSession
from fsm.states import FSMAdmin
from keyboards.keyboards import add_incident
from lexicon.lexicon import lexicon
from lexicon.lexicon import admin_menu_lexicon
from database import requests as rq
from services.services import create_excel
from utils.utils import get_output_filename


logger = logging.getLogger(__name__)


async def logout_from_admin(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    await callback.message.answer("Ты вышел из меню админа.")
    await callback.message.answer(text=lexicon["new"], reply_markup=add_incident())
    await dialog_manager.done()


async def first_date_process(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    clicked_date: date,
    /,
):
    serial_date = clicked_date.strftime("%d.%m.%Y")
    dialog_manager.dialog_data.update(first_date_excel=serial_date)
    await dialog_manager.next()


async def last_date_process(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    clicked_date: date,
    /,
):
    serial_date = clicked_date.strftime("%d.%m.%Y")
    dialog_manager.dialog_data.update(last_date_excel=serial_date)


async def del_last_date(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data.update(last_date_excel=None)


async def del_first_date(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    dialog_manager.dialog_data.update(first_date_excel=None)


async def download_excel(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
):
    first_date_excel = dialog_manager.dialog_data.get("first_date_excel")
    last_date_excel = dialog_manager.dialog_data.get("last_date_excel")

    dates = (
        datetime.strptime(d, "%d.%m.%Y") for d in [first_date_excel, last_date_excel]
    )

    session = dialog_manager.middleware_data.get("session")
    result = await rq.get_incedents(
        *dates,
        session=session,
    )
    output_filename = get_output_filename(first_date_excel, last_date_excel)

    file_path = create_excel(result, output_filename)
    await callback.message.answer_document(
        FSInputFile(file_path), caption="Отчет выгружен!"
    )
    os.remove(file_path)
    await dialog_manager.start(state=FSMAdmin.main_menu, mode=StartMode.RESET_STACK)


async def selection_getter(dialog_manager: DialogManager, **_):
    first_date = dialog_manager.dialog_data.get("first_date_excel", None)
    last_date = dialog_manager.dialog_data.get("last_date_excel", None)
    download_status = bool(first_date) and bool(last_date)
    return {
        "first_date_excel": first_date,
        "last_date_excel": last_date,
        "download_status": download_status,
    }


admin_dialog = Dialog(
    Window(
        Const(admin_menu_lexicon["admin_correct"]),
        Next(text=Const("Выгрузить Excel"), id="on_calendar_page"),
        Button(text=Const("Выйти"), id="quit_button", on_click=logout_from_admin),
        state=FSMAdmin.main_menu,
    ),
    Window(
        Multi(
            Const(text="Выбери дату начала выгрузки."),
            Format(text="Начало: {first_date_excel}\nКонец: {last_date_excel}"),
            sep="\n\n",
        ),
        Calendar(id="calendar", on_click=first_date_process),
        Back(text=Const("Назад"), id="back", on_click=del_first_date),
        state=FSMAdmin.first_date,
        getter=selection_getter,
    ),
    Window(
        Multi(
            Const(text="Выбери дату конца выгрузки."),
            Format(text="Начало: {first_date_excel}\nКонец: {last_date_excel}"),
            sep="\n\n",
        ),
        Calendar(id="calendar", on_click=last_date_process),
        Button(
            text=Const("Загрузить"),
            id="download",
            on_click=download_excel,
            when="download_status",
        ),
        Back(text=Const("Назад"), id="back_2", on_click=del_last_date),
        state=FSMAdmin.last_date,
        getter=selection_getter,
    ),
)
