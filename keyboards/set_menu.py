from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


user_menu: dict = {
    "/start": "Перезапустить бота",
    "/cancel": "Отменить заполнение инцидента",
}

admin_menu: dict = {
    "/start": "Перезапустить бота",
    "/cancel": "Отменить заполнение инцидента",
    "/admin": "Открыть меню администратора",
}


async def set_user_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in user_menu.items()
    ]
    await bot.set_my_commands(main_menu_commands)


async def set_admin_menu(admin_ids, bot: Bot):
    for admin in admin_ids:
        adm_commands = [
            BotCommand(command=command, description=description)
            for command, description in admin_menu.items()
        ]
        await bot.set_my_commands(
            adm_commands, scope=BotCommandScopeChat(chat_id=admin)
        )
