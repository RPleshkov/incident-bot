from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


from fsm.states import FSMAdmin
from lexicon.lexicon import lexicon

router = Router(name="admin_handlers_router")
router.callback_query.filter(StateFilter(FSMAdmin))
router.message.filter(StateFilter(FSMAdmin))


@router.callback_query(F.data == "quit")
async def quit_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=lexicon['quit'])
    await state.clear()



@router.callback_query(F.data == 'get_excel')
async def quit_admin(callback: CallbackQuery, state: FSMContext):
    pass



@router.message()
async def trash_handler(message: Message):
    await message.answer(text="ты в админке")
