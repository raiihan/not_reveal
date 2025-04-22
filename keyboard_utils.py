from telegram import ReplyKeyboardMarkup, KeyboardButton, BotCommand

def get_user_keyboard():
    keyboard = [
        [KeyboardButton("📁 Start")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_admin_keyboard():
    keyboard = [
        [KeyboardButton("📁 Start")],
        [KeyboardButton("🔗 Generate Link"), KeyboardButton("📦 Batch Upload")],
        [KeyboardButton("👥 Admin List"), KeyboardButton("🗑️ Delete File")],
        [KeyboardButton("📊 Bot Stats"), KeyboardButton("📣 Broadcast")],
        [KeyboardButton("👤 User Details")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)




async def set_bot_commands(application):
    commands = [
        BotCommand("start", "Start bot"),
        BotCommand("genlink", "Generate deep link"),
        BotCommand("batch", "Batch upload files"),
        BotCommand("delete", "Delete file"),
        BotCommand("broadcast", "Send message to all users"),
        BotCommand("user", "Show user details"),
        BotCommand("stats", "Show bot stats"),
        BotCommand("help", "Show help"),
    ]


