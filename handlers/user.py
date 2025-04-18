import logging
from aiogram.exceptions import TelegramBadRequest
from datetime import datetime
from aiogram import Bot, Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from fluentogram import TranslatorRunner
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession
from filters.filters import DateTimeFilter, HospNameFilter, IsAdmin
from keyboards.keyboards import *
from fsm.states import FSMAdmin, FSMFillIncident
from services.services import mess_cleaner
from utils.utils import confirm_form, confirm_form_edited
from database import requests as rq

router = Router(name="user_handlers_router")
logger = logging.getLogger(__name__)


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start_process(
    message: Message, session: AsyncSession, i18n: TranslatorRunner
):
    if message.from_user:
        await rq.upsert_user(
            session,
            message.from_user.id,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        await message.answer(
            text=i18n.start(first_name=message.from_user.first_name),
            reply_markup=add_incident(),
        )


@router.message(~StateFilter(default_state), Command("cancel"))
async def cmd_cancel_process(
    message: Message, state: FSMContext, i18n: TranslatorRunner
):
    await message.answer(text=i18n.cancel())
    await message.answer(text=i18n.new(), reply_markup=add_incident())
    await state.clear()


@router.message(Command("admin"), ~StateFilter(FSMFillIncident), IsAdmin())
async def cmd_admin_process_correct(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=FSMAdmin.main_menu, mode=StartMode.RESET_STACK)


@router.message(Command("admin"), IsAdmin())
async def cmd_admin_process_incorrect(message: Message, i18n: TranslatorRunner):
    await message.answer(text=i18n.admin_incorrect())


@router.callback_query(StateFilter(default_state), F.data == "add_incident")
async def start_add_incident(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner
):
    await callback.answer()
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    await state.update_data(current_time=current_time)
    if callback.message:
        answer = await callback.message.answer(
            text=i18n.add_incident(), reply_markup=current_time_kb(current_time)
        )
        mess2ass = await mess_cleaner(answer.message_id)
        await state.update_data(mess2ass)
        await state.set_state(FSMFillIncident.time)


@router.message(
    StateFilter(FSMFillIncident.time),
    DateTimeFilter(),
)
async def time_handler_correct(
    message: Message, state: FSMContext, i18n: TranslatorRunner, time: str
):
    await state.update_data(time=time)
    answer = await message.answer(text=i18n.hosp_name())
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)
    await state.set_state(FSMFillIncident.hosp_name)


@router.callback_query(StateFilter(FSMFillIncident.time), F.data == "current_time_btn")
async def current_time_btn_process(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner
):
    await callback.answer()
    await state.update_data(time=await state.get_value("current_time"))
    answer = await callback.message.answer(text=i18n.hosp_name())
    mess2ass = await mess_cleaner(answer.message_id)
    await state.update_data(mess2ass)
    await state.set_state(FSMFillIncident.hosp_name)


@router.message(StateFilter(FSMFillIncident.time))
async def time_handler_incorrect(
    message: Message, i18n: TranslatorRunner, state: FSMContext
):
    answer = await message.answer(text=i18n.incorrect_time())
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)


@router.message(StateFilter(FSMFillIncident.hosp_name), HospNameFilter())
async def hosp_name_handler_correct(
    message: Message, state: FSMContext, i18n: TranslatorRunner, hosp_name: str
):
    await state.update_data(hosp_name=hosp_name)
    answer = await message.answer(text=i18n.inc_number())
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)
    await state.set_state(FSMFillIncident.inc_number)


@router.message(StateFilter(FSMFillIncident.hosp_name))
async def hosp_name_handler_incorrect(
    message: Message, i18n: TranslatorRunner, state: FSMContext
):
    answer = await message.answer(text=i18n.hosp_name_incorrect())
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)


@router.message(
    StateFilter(FSMFillIncident.inc_number),
    F.text.regexp(r"INC\d{6}") | F.text.regexp(r"REQ\d{6}"),
)
async def inc_number_handler_correct(
    message: Message, state: FSMContext, i18n: TranslatorRunner
):
    await state.update_data(inc_number=message.text)
    answer = await message.answer(text=i18n.sti_res(), reply_markup=sti_res_kb())
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)
    await state.set_state(FSMFillIncident.sti_res)


@router.message(StateFilter(FSMFillIncident.inc_number))
async def inc_number_handler_incorrect(
    message: Message, i18n: TranslatorRunner, state: FSMContext
):
    answer = await message.answer(text=i18n.inc_number_incorrect())
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)


@router.callback_query(
    StateFilter(FSMFillIncident.sti_res),
    F.data == "sti_yes",
)
async def sti_res_handler_yes(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner
):
    await callback.answer()
    await state.update_data(sti_res=True)
    if callback.message:
        answer = await callback.message.answer(text=i18n.inc_child_number())
        mess2ass = await mess_cleaner(answer.message_id)
        await state.update_data(mess2ass)
        await state.set_state(FSMFillIncident.inc_child_number)


@router.message(
    StateFilter(FSMFillIncident.inc_child_number),
    F.text.regexp(r"INC\d{6}") | F.text.regexp(r"REQ\d{6}"),
)
async def inc_child_number_handler_correct(
    message: Message, state: FSMContext, i18n: TranslatorRunner
):
    await state.update_data(inc_child_number=message.text)
    answer = await message.answer(text=i18n.description())
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)
    await state.set_state(FSMFillIncident.description)


@router.message(StateFilter(FSMFillIncident.inc_child_number))
async def inc_child_number_handler_incorrect(
    message: Message, i18n: TranslatorRunner, state: FSMContext
):
    answer = await message.answer(text=i18n.inc_number_incorrect())
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)


@router.callback_query(
    StateFilter(FSMFillIncident.sti_res),
    F.data == "sti_no",
)
async def sti_res_handler_no(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner
):
    await callback.answer()
    await state.update_data(sti_res=False, inc_child_number=None)
    if callback.message:
        answer = await callback.message.answer(text=i18n.description())
        mess2ass = await mess_cleaner(answer.message_id)
        await state.update_data(mess2ass)
        await state.set_state(FSMFillIncident.description)


@router.message(StateFilter(FSMFillIncident.description), F.text)
async def description_handler(
    message: Message, state: FSMContext, i18n: TranslatorRunner
):
    await state.update_data(description=message.text)
    answer = await message.answer(text=i18n.resolution())
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)
    await state.set_state(FSMFillIncident.resolution)


@router.message(StateFilter(FSMFillIncident.resolution), F.text)
async def resolution_handler(message: Message, state: FSMContext):
    await state.update_data(resolution=message.text)
    answer = await message.answer(
        text=confirm_form(await state.get_data()), reply_markup=confirm_or_refill()
    )
    mess2ass = await mess_cleaner(answer.message_id, message.message_id)
    await state.update_data(mess2ass)
    await state.update_data(confirmed_message=answer.message_id)
    await state.set_state(FSMFillIncident.confirmation)


@router.callback_query(
    StateFilter(FSMFillIncident.confirmation), F.data == "refil_pressed"
)
async def refil_btn_process(
    callback: CallbackQuery, state: FSMContext, i18n: TranslatorRunner, bot: Bot
):
    await callback.answer()
    data = await state.get_data()
    await bot.delete_messages(
        callback.message.chat.id,
        [v for k, v in data.items() if k.startswith("mess_")],
    )
    if callback.message:
        answer = await callback.message.answer(
            text=i18n.add_incident(), reply_markup=current_time_kb(data["current_time"])
        )
        mess2ass = await mess_cleaner(answer.message_id)
        await state.update_data(mess2ass)
        await state.set_state(FSMFillIncident.time)


@router.callback_query(
    StateFilter(FSMFillIncident.confirmation), F.data == "confirm_pressed"
)
async def confirm_btn_process(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    i18n: TranslatorRunner,
    bot: Bot,
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
        try:
            await bot.delete_messages(
                callback.message.chat.id,
                [v for k, v in data.items() if k.startswith('mess_')],
            )
        except TelegramBadRequest:
            pass
        finally:
            await callback.message.answer(
                confirm_form_edited(data),
            )
            await state.clear()
            answer = await callback.message.answer(
                text=i18n.new(), reply_markup=add_incident()
            )
            mess2ass = await mess_cleaner(answer.message_id)
            await state.update_data(mess2ass)
