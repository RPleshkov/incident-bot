import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from filters.filters import DateTimeFilter, HospNameFilter, IsAdmin
from keyboards.keyboards import *
from fsm.states import FSMAdmin, FSMFillIncident
from lexicon.lexicon import lexicon
from utils.utils import confirm_form
from database import requests as rq

router = Router(name="user_handlers_router")
logger = logging.getLogger(__name__)


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start_process(message: Message, session: AsyncSession):
    if message.from_user:
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


@router.message(Command("admin"), ~StateFilter(FSMFillIncident), IsAdmin())
async def cmd_admin_process_correct(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=FSMAdmin.main_menu, mode=StartMode.RESET_STACK)


@router.message(Command("admin"), IsAdmin())
async def cmd_admin_process_incorrect(message: Message):
    await message.answer(text=lexicon["admin_incorrect"])


@router.callback_query(StateFilter(default_state), F.data == "add_incident")
async def start_add_incident(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.message:
        await callback.message.answer(text=lexicon["add_incident"])
        await state.set_state(FSMFillIncident.time)


@router.message(
    StateFilter(FSMFillIncident.time),
    DateTimeFilter(),
)
async def time_handler_correct(message: Message, state: FSMContext, time):
    await state.update_data(time=time)
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


@router.message(
    StateFilter(FSMFillIncident.inc_number),
    F.text.regexp(r"INC\d{6}") | F.text.regexp(r"REQ\d{6}"),
)
async def inc_number_handler_correct(message: Message, state: FSMContext):
    await state.update_data(inc_number=message.text)
    await message.answer(text=lexicon["sti_res"], reply_markup=sti_res_kb())
    await state.set_state(FSMFillIncident.sti_res)


@router.message(StateFilter(FSMFillIncident.inc_number))
async def inc_number_handler_incorrect(message: Message):
    await message.answer(text=lexicon["inc_number_incorrect"])


@router.callback_query(
    StateFilter(FSMFillIncident.sti_res),
    F.data == "sti_yes",
)
async def sti_res_handler_yes(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(sti_res=True)
    if callback.message:
        await callback.message.answer(text=lexicon["inc_child_number"])
        await state.set_state(FSMFillIncident.inc_child_number)


@router.message(
    StateFilter(FSMFillIncident.inc_child_number),
    F.text.regexp(r"INC\d{6}") | F.text.regexp(r"REQ\d{6}"),
)
async def inc_child_number_handler_correct(message: Message, state: FSMContext):
    await state.update_data(inc_child_number=message.text)
    await message.answer(text=lexicon["description"])
    await state.set_state(FSMFillIncident.description)


@router.message(StateFilter(FSMFillIncident.inc_child_number))
async def inc_child_number_handler_incorrect(message: Message):
    await message.answer(text=lexicon["inc_number_incorrect"])


@router.callback_query(
    StateFilter(FSMFillIncident.sti_res),
    F.data == "sti_no",
)
async def sti_res_handler_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(sti_res=False, inc_child_number=None)
    if callback.message:
        await callback.message.answer(text=lexicon["description"])
        await state.set_state(FSMFillIncident.description)


@router.message(StateFilter(FSMFillIncident.description), F.text)
async def description_handler(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text=lexicon["resolution"])
    await state.set_state(FSMFillIncident.resolution)


@router.message(StateFilter(FSMFillIncident.resolution), F.text)
async def resolution_handler(message: Message, state: FSMContext):
    await state.update_data(resolution=message.text)
    await message.answer(
        text=confirm_form(await state.get_data()), reply_markup=confirm_or_refill()
    )
    await state.set_state(FSMFillIncident.confirmation)


@router.callback_query(
    StateFilter(FSMFillIncident.confirmation), F.data == "refil_pressed"
)
async def refil_btn_process(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.message:
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
        time=datetime.strptime(data["time"], "%d.%m.%Y %H:%M:%S"),
        hosp_name=data["hosp_name"],
        inc_number=data["inc_number"],
        inc_child_number=data["inc_child_number"],
        description=data["description"],
        resolution=data["resolution"],
        sti_res=data["sti_res"],
        creator=callback.from_user.id,
    )
    if callback.message:
        await callback.message.answer(text=lexicon["confirm_pressed"])
        await callback.message.answer(text=lexicon["new"], reply_markup=add_incident())
        await state.clear()
