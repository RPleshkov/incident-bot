from aiogram.fsm.state import State, StatesGroup


class FSMFillIncident(StatesGroup):
    time = State()
    hosp_name = State()
    inc_number = State()
    description = State()
    resolution = State()
    confirmation = State()
