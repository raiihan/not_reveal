from telegram import Update
from telegram.ext import ContextTypes
from keyboard_utils import get_user_keyboard, get_admin_keyboard
from config import ADMIN_IDS  # [Your Telegram ID and other admin IDs]

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.callback_query.message
    user_id = message.from_user.id

    try:
        await message.delete()  # auto delete previous message
    except Exception:
        pass

    if user_id in ADMIN_IDS:
        await context.bot.send_message(
            chat_id=message.chat_id,
            text="👋 Hello Admin! Choose an option from below 👇",
            reply_markup=get_admin_keyboard()
        )
    else:
        await context.bot.send_message(
            chat_id=message.chat_id,
            text="👋 Welcome! You can use this bot to download files via links.\nOnly admins can manage files.",
            reply_markup=get_user_keyboard()
        )
