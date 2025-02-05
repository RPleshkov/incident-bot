import datetime


def confirm_form(data: dict):

    if data["restart_platform"] is True:
        res = "✅"
    if data["restart_platform"] is False:
        res = "❌"

    form = (
        f"<b>Проверь корректность заполненных данных</b>:\n\n"
        + f"<b>Дата/Время</b>: {eval(data['time'])}\n"
        + f"<b>МО</b>: {data['hosp_name']}\n"
        + f"<b>Номер INC</b>: {data['inc_number']}\n"
        + f"<b>Краткое описание проблемы</b>: {data['description']}\n"
        + f"<b>Решение</b>: {data['resolution']}\n"
        + f"<b>Рестарт платформы</b>: {res}"
    )

    return form
