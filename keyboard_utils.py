from telegram import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from telegram.error import BadRequest

ADMINS = [1615680044, 5621290261, 5765156518]

async def set_bot_commands(application):
    # Commands for all users
    user_commands = [
        BotCommand("start", "📁 Start"),
        BotCommand("help", "ℹ️ Get help"),
    ]
    await application.bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    # Commands for admin users
    admin_commands = [
        BotCommand("genlink", "🔗 Generate link"),
        BotCommand("editfile", "📝 Edit file"),
        BotCommand("batchupload", "📦 Upload multiple files"),
        BotCommand("delete", "🗑️ Delete file"),
        BotCommand("adminlist", "👥 Admin list"),
        BotCommand("stats", "📊 Bot stats"),
        BotCommand("user", "👤 User info"),
        BotCommand("broadcast", "📣 Broadcast"),
    ]

    # Safe way to set commands per admin
    for admin_id in ADMINS:
        try:
            await application.bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin_id))
        except BadRequest as e:
            print(f"❗ Skipping admin {admin_id}: {e}")
