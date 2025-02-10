def confirm_form(data: dict):

    if data["sti_res"] is True:
        res = "✅"
    if data["sti_res"] is False:
        res = "❌"

    form = (
        f"<b>Проверь корректность заполненных данных</b>:\n\n"
        + f"<b>Дата/Время</b>: {data['time']}\n"
        + f"<b>МО</b>: {data['hosp_name']}\n"
        + f"<b>Решено СТИ</b>: {res}\n"
        + f"<b>Номер заявки</b>: {data['inc_number']}\n"
        + f"<b>Номер дочерней заявки</b>: {data['inc_child_number']}\n"
        + f"<b>Краткое описание проблемы</b>: {data['description']}\n"
        + f"<b>Решение</b>: {data['resolution']}\n"
    )

    return form


def confirm_form_edited(data: dict):

    if data["sti_res"] is True:
        res = "✅"
    if data["sti_res"] is False:
        res = "❌"

    form = (
        f"<b>Инцидент зафиксирован!</b>\n\n"
        + f"<b>Дата/Время</b>: {data['time']}\n"
        + f"<b>МО</b>: {data['hosp_name']}\n"
        + f"<b>Решено СТИ</b>: {res}\n"
        + f"<b>Номер заявки</b>: {data['inc_number']}\n"
        + f"<b>Номер дочерней заявки</b>: {data['inc_child_number']}\n"
        + f"<b>Краткое описание проблемы</b>: {data['description']}\n"
        + f"<b>Решение</b>: {data['resolution']}\n"
    )

    return form


def get_output_filename(
    first_date: str,
    last_date: str,
) -> str:
    return f"Массовые инциденты {first_date}-{last_date}.xlsx"


def create_text_summary_from_data(
    data: list[tuple], first_date: str, last_date: str
) -> str:

    sti_resolved_hospitals = set()
    self_resolved_hospitals = set()

    for row in data:
        if row[3] is None:
            self_resolved_hospitals.add(row[1])
        else:
            sti_resolved_hospitals.add(tuple([row[3], row[1], row[5]]))

    sti_resolved_hospital_strings = [
        f"<u>{child_inc}</u> - {hosp_name}\n{resolve}\n"
        for child_inc, hosp_name, resolve in sti_resolved_hospitals
    ]

    text = (
        "Доброе утро!\n\n"
        + f"<b>{first_date}-{last_date}</b>\nБыли рестарты сервисов в следующих МО:\n\n"
        + f'{"\n".join(self_resolved_hospitals)}\n\n'
        + "<b>Решено СТИ:</b>\n\n"
        + f'{"\n".join(sti_resolved_hospital_strings)}'
    )

    return text
