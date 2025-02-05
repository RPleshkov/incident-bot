def confirm_form(data: dict):

    form = (
        f"<b>Проверь корректность заполненных данных</b>:\n\n"
        + f"<b>Дата/Время</b>: {data['time']}\n"
        + f"<b>МО</b>: {data['hosp_name']}\n"
        + f"<b>Номер INC</b>: {data['inc_number']}\n"
        + f"<b>Краткое описание проблемы</b>: {data['description']}\n"
        + f"<b>Решение</b>: {data['resolution']}\n"
    )

    return form



