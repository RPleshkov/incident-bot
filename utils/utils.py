import datetime


def confirm_form(data: dict):

    if data["sti_res"] is True:
        res = "✅"
    if data["sti_res"] is False:
        res = "❌"

    form = (
        f"<b>Проверь корректность заполненных данных</b>:\n\n"
        + f"<b>Дата/Время</b>: {eval(data['time'])}\n"
        + f"<b>МО</b>: {data['hosp_name']}\n"
        + f"<b>Решено СТИ</b>: {res}\n"
        + f"<b>Номер заявки</b>: {data['inc_number']}\n"
        + f"<b>Номер дочерней заявки</b>: {data['inc_child_number']}\n"
        + f"<b>Краткое описание проблемы</b>: {data['description']}\n"
        + f"<b>Решение</b>: {data['resolution']}\n"
    )

    return form


def get_output_filename(
    first_date,
    last_date,
) -> str:
    first_date = datetime.datetime.strftime(eval(first_date), "%d.%m")
    last_date = datetime.datetime.strftime(eval(last_date), "%d.%m.%Y")
    return f"Массовые инциденты {first_date}-{last_date}.xlsx"
