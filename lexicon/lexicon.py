from datetime import datetime


current_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

lexicon = {
    "/start": "<b>Привет!</b>\n\n"
    "Данный бот позволяет фиксировать информацию о массовых инцидентах.\n\n"
    "Жми на кнопку ниже, чтобы внести информацию.",
    "/cancel": "Заполнение отменено.",
    "add_incident": f"Отправь мне дату и время инцидента в формате указанном ниже:\n\n"
    f"<b>{current_date}</b>",
    "hosp_name": "Укажи код МО",
    "inc_number": "Пришли номер заявки в формате:\n\nINC100100 или REQ100100",
    "inc_number_incorrect": "Неверно указан формат!",
    "sti_res": "Заявку решали СТИ?",
    "inc_child_number": "Пришли номер дочерней заявки в формате:\n\nINC100100 или REQ100100",
    "description": "Составь краткое описание проблемы.",
    "resolution": "Какое решение было предпринято?",
    "confirm_pressed": "Готово!",
    "new": "Жми на кнопку, чтобы зафиксировать новый инцидент.",
    "incorrect_time": "<b>Некорректный формат!</b>\n\nДата должна быть в формате указанном ниже:\n\n"
    f"<b>{current_date}</b>",
    "hosp_name_incorrect": "<b>Некорректный формат, или нет МО с таким кодом!</b>",
    "admin_correct": "Добро пожаловать в меню админа!",
    "admin_incorrect": "Чтобы войти в меню админа - закончи заполнение инцидента, либо отмени заполнение командой /cancel",
    "quit": "Вы вышли из меню администратора.",
}
