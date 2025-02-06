from aiogram.fsm.state import State, StatesGroup


class FSMFillIncident(StatesGroup):
    time = State()
    hosp_name = State()
    inc_number = State()
    sti_res = State()
    inc_child_number = State()
    description = State()
    resolution = State()
    confirmation = State()


class FSMAdmin(StatesGroup):
    admin_mode = State()

    first_date_excel = State()
    last_date_excel = State()
