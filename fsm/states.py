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
    main_menu = State()
    first_date = State()
    last_date = State()
    excel_done = State()
