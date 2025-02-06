import os
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    Message,
)
from sqlalchemy.ext.asyncio import AsyncSession


from filters.filters import DateTimeFilter
from fsm.states import FSMAdmin
from lexicon.lexicon import lexicon
from database import requests as rq
import datetime
from services.services import create_excel
from utils.utils import get_output_filename


router = Router(name="admin_handlers_router")
router.callback_query.filter(StateFilter(FSMAdmin))
router.message.filter(StateFilter(FSMAdmin))


@router.callback_query(F.data == "quit")
async def quit_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=lexicon["quit"])
    await state.clear()


@router.callback_query(F.data == "get_excel")
async def get_excel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=lexicon["first_date_excel"])
    await state.set_state(FSMAdmin.first_date_excel)


@router.message(
    StateFilter(FSMAdmin.first_date_excel),
    DateTimeFilter(),
)
async def first_date_excel_correct(message: Message, state: FSMContext, time):
    await state.update_data(first_date_excel=time)
    await message.answer(text=lexicon["last_date_excel"])
    await state.set_state(FSMAdmin.last_date_excel)


@router.message(StateFilter(FSMAdmin.first_date_excel))
async def first_date_excel_incorrect(message: Message):
    await message.answer(text=lexicon["incorrect_time"])


@router.message(
    StateFilter(FSMAdmin.last_date_excel),
    DateTimeFilter(),
)
async def last_date_excel_correct(
    message: Message, state: FSMContext, session: AsyncSession, time
):
    await state.update_data(last_date_excel=time)
    """Здесь должен быть запрос в бд"""
    data = await state.get_data()
    result = await rq.get_incedents(
        session=session,
        first_date_excel=eval(data["first_date_excel"]),
        last_date_excel=eval(data["last_date_excel"]),
    )
    output_filename = get_output_filename(
        data["first_date_excel"], data["last_date_excel"]
    )
    file_path = create_excel(result, output_filename)
    await message.answer_document(FSInputFile(file_path))
    os.remove(file_path)
    await state.set_state(FSMAdmin.admin_mode)


@router.message(StateFilter(FSMAdmin.last_date_excel))
async def last_date_excel_incorrect(message: Message):
    await message.answer(text=lexicon["incorrect_time"])


@router.message()
async def trash_handler(message: Message):
    await message.answer(text="ты в админке")
