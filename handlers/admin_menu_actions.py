from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS

async def handle_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = message.from_user.id

    if user_id not in ADMIN_IDS:
        await message.reply_text("🚫 You are not allowed to perform this action.")
        return

    text = message.text

    if text == "👥 Admin List":
        admin_list = "\n".join([f"👤 `{admin_id}`" for admin_id in ADMIN_IDS])
        await message.reply_text(f"🔐 Current Admins:\n{admin_list}", parse_mode="Markdown")

    elif text == "🔗 Generate Link":
        await message.reply_text("📤 Please send a file to generate a deep link.")

    elif text == "📦 Batch Upload":
        await message.reply_text("📥 Send multiple files for batch upload...")

    elif text == "🗑️ Delete File":
        await message.reply_text("❌ Please send file ID to delete.")

    elif text == "📢 Broadcast":
        await message.reply_text("📨 Please send your message to broadcast.")

    elif text == "🧾 User Details":
        await message.reply_text("🧐 Send user ID to get details.")

    elif text == "📊 Bot Stats":
        await message.reply_text("📈 Collecting bot stats...")

    elif text == "↩️ Back":
        await message.delete()
        await context.bot.send_message(
            chat_id=message.chat_id,
            text="⬅️ Menu returned.",
            reply_markup=get_admin_keyboard()
        )
