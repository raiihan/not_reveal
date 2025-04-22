from telegram import ReplyKeyboardMarkup, KeyboardButton

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
