import asyncio
from email import message
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from filters.filters import HospNameFilter
from keyboards.keyboards import *
from fsm.states import FSMFillIncident
from lexicon.lexicon import lexicon
from utils.utils import confirm_form, str_to_datetime
from database import requests as rq

router = Router(name="user_handlers_router")


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start_process(message: Message, session: AsyncSession):
    await rq.upsert_user(
        session,
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name,
    )
    await message.answer(text=lexicon["/start"], reply_markup=add_incident())


@router.message(~StateFilter(default_state), Command("cancel"))
async def cmd_cancel_process(message: Message, state: FSMContext):
    await message.answer(text=lexicon["/cancel"])
    await message.answer(text=lexicon["new"], reply_markup=add_incident())
    await state.clear()


@router.callback_query(StateFilter(default_state), F.data == "add_incident")
async def start_add_incident(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=lexicon["add_incident"])
    await state.set_state(FSMFillIncident.time)


@router.message(
    StateFilter(FSMFillIncident.time),
    F.text.regexp(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}"),
)
async def time_handler_correct(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer(text=lexicon["hosp_name"])
    await state.set_state(FSMFillIncident.hosp_name)


@router.message(StateFilter(FSMFillIncident.time))
async def time_handler_incorrect(message: Message):
    await message.answer(text=lexicon["incorrect_time"])


@router.message(StateFilter(FSMFillIncident.hosp_name), HospNameFilter())
async def hosp_name_handler_correct(message: Message, state: FSMContext, hosp_name):
    await state.update_data(hosp_name=hosp_name)
    await message.answer(text=lexicon["inc_number"])
    await state.set_state(FSMFillIncident.inc_number)


@router.message(StateFilter(FSMFillIncident.hosp_name))
async def hosp_name_handler_incorrect(message: Message):
    await message.answer(text=lexicon["hosp_name_incorrect"])


@router.message(StateFilter(FSMFillIncident.inc_number), F.text.regexp(r"INC\d{6}"))
async def inc_number_handler_correct(message: Message, state: FSMContext):
    await state.update_data(inc_number=message.text)
    await message.answer(text=lexicon["description"])
    await state.set_state(FSMFillIncident.description)


@router.message(StateFilter(FSMFillIncident.inc_number))
async def inc_number_handler_incorrect(message: Message):
    await message.answer(text=lexicon["inc_number_incorrect"])


@router.message(StateFilter(FSMFillIncident.description), F.text)
async def description_handler(message: Message, state: FSMContext):
    print(message)
    await state.update_data(description=message.text)
    await message.answer(text=lexicon["resolution"])
    await state.set_state(FSMFillIncident.resolution)


@router.message(StateFilter(FSMFillIncident.resolution), F.text)
async def resolution_handler(message: Message, state: FSMContext):
    await state.update_data(resolution=message.text)
    await message.answer(
        text=lexicon["restart_platform"], reply_markup=restart_platform_kb()
    )
    await state.set_state(FSMFillIncident.restart_platform)


@router.callback_query(
    StateFilter(FSMFillIncident.restart_platform),
    F.data.in_(["restart_yes", "restart_no"]),
)
async def restart_platform_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "restart_yes":
        res = True
    if callback.data == "restart_no":
        res = False

    await state.update_data(restart_platform=res)
    await callback.message.answer(
        text=confirm_form(await state.get_data()), reply_markup=confirm_or_refill()
    )
    await state.set_state(FSMFillIncident.confirmation)


@router.callback_query(
    StateFilter(FSMFillIncident.confirmation), F.data == "refil_pressed"
)
async def refil_btn_process(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=lexicon["add_incident"])
    await state.clear()
    await state.set_state(FSMFillIncident.time)


@router.callback_query(
    StateFilter(FSMFillIncident.confirmation), F.data == "confirm_pressed"
)
async def confirm_btn_process(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    await callback.answer()
    data = await state.get_data()
    await rq.set_incident(
        session=session,
        time=str_to_datetime(data["time"]),
        hosp_name=data["hosp_name"],
        inc_number=data["inc_number"],
        description=data["description"],
        resolution=data["resolution"],
        restart_platform=data["restart_platform"],
        creator=callback.from_user.id,
    )
    await callback.message.answer(text=lexicon["confirm_pressed"])
    await callback.message.answer(text=lexicon["new"], reply_markup=add_incident())
    await state.clear()
