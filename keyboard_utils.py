from telegram import BotCommand, BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeChat

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
    for admin_id in ADMINS:
        await application.bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin_id))
