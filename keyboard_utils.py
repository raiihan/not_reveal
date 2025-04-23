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
        [InlineKeyboardButton("📝 Edit File Description", callback_data='edit_file')],
        [InlineKeyboardButton("📊 Bot Stats", callback_data='view_stats')],
        [InlineKeyboardButton("📁 Batch Upload", callback_data='batch_upload')]
        [KeyboardButton("👤 User Details")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)






async def set_bot_commands(application):
    commands = [
        BotCommand("start", "Start the bot"),
        
        BotCommand("genlink", "Upload & get a deep link"),
        BotCommand("batch_upload", "Upload multiple files"),
        BotCommand("delete", "Delete file"),
        BotCommand("adminlist", "Admin List"),
        BotCommand("stats", "View bot statistics"),
        BotCommand("editfile", "Edit file description"),
        BotCommand("broadcast", "Send message to all users"),
        BotCommand("user", "Show user details"),
    ]
    await application.bot.set_my_commands(commands)

