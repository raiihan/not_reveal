from telegram import BotCommand

async def set_bot_commands(application):
    commands = [
        BotCommand("start", "📁 Start the bot"),
        BotCommand("genlink", "🔗 Generate a deep link"),
        BotCommand("editfile", "📝 Edit file description"),
        BotCommand("batchupload", "📦 Upload multiple files"),
        BotCommand("delete", "🗑️ Delete a file"),
        BotCommand("adminlist", "👥 List of bot admins"),
        BotCommand("stats", "📊 View bot stats"),
        BotCommand("user", "👤 View user info"),
        BotCommand("broadcast", "📣 Broadcast a message"),
    ]
    await application.bot.set_my_commands(commands)

