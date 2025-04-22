from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_user_keyboard():
    """Keyboard for regular users (download-only access)."""
    keyboard = [
        [InlineKeyboardButton("📥 Sample File", url="https://t.me/NotRevealBot?start=1")],
        [InlineKeyboardButton("ℹ️ How It Works", callback_data="info")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_keyboard():
    """Keyboard for bot admins/owner (full control)."""
    keyboard = [
        [InlineKeyboardButton("🔗 Generate Link", callback_data="generate_link")],
        [InlineKeyboardButton("📦 Batch Upload", callback_data="batch_upload")],
        [InlineKeyboardButton("🧑‍💻 Admin List", callback_data="admin_list")],
        [InlineKeyboardButton("🗑️ Delete File", callback_data="delete_file")],
        [InlineKeyboardButton("📊 Bot Stats", callback_data="bot_stats")],
        [InlineKeyboardButton("📢 Broadcast Message", callback_data="broadcast")],
        [InlineKeyboardButton("👤 User Details", callback_data="user_details")]
    ]
    return InlineKeyboardMarkup(keyboard)
