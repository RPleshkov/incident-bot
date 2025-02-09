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
    print(first_date, last_date)
    return f"Массовые инциденты {first_date}-{last_date}.xlsx"


def create_text_summary_from_data(
    data: list[tuple], first_date: str, last_date: str
) -> str:

    sti_resolved_hospitals: set[tuple] = set()
    self_resolved_hospitals: set[str] = set()

    for row in data:
        if row[3] is None:
            self_resolved_hospitals.add(row[1])
        else:
            info = tuple([row[3], row[1], row[5]])
            sti_resolved_hospitals.add(info)

    formatted_sti_resolved_hospitals = [
        f"<u>{inc_child}</u> - {hosp_name}\nРешение: {resolve}"
        for inc_child, hosp_name, resolve in sti_resolved_hospitals
    ]

    text = (
        "Доброе утро!\n\n"
        + f"<b>{first_date}-{last_date}</b>\nБыли рестарты сервисов в следующих МО:\n\n"
        + f'{'\n'.join(self_resolved_hospitals)}\n\n'
        + f"<b>Эскалированные на СТИ:</b>\n\n"
        + f"{'\n\n'.join(formatted_sti_resolved_hospitals)}"
    )

    return text
