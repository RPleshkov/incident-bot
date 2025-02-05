from datetime import datetime


current_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

lexicon = {
    "/start": "<b>Привет!</b>\n\n"
    "Данный бот позволяет фиксировать информацию о массовых инцидентах.\n\n"
    "Жми на кнопку ниже, чтобы внести информацию.",
    '/cancel': 'Заполнение отменено.',
    "add_incident": f"Отправь мне дату и время инцидента в формате указанном ниже:\n\n"
    f"<b>{current_date}</b>",
    "hosp_name": "Укажи название МО. Желательно скопирировать полное название из Naumen.",
    "inc_number": "Пришли номер инцидента в формате <b>INC100100</b>",
    "description": "Составь краткое описание проблемы.",
    "resolution": "Какое решение было предпринято?",
    "confirm_pressed": "Инцидент зафиксирован!",
}
