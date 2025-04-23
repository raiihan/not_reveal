from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CommandHandler
from telegram.constants import ParseMode
from telegram.ext import filters
from utils.stats import get_stats
import logging
from utils.admin_IDs import ADMIN_IDs


logger = logging.getLogger(__name__)

ASK_MESSAGE = 1

ADMINS = [1615680044]  # Replace with your admin IDs

async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDs:
        await update.message.reply_text("🚫 Only admins can use this command.")
        return ConversationHandler.END

    await update.message.reply_text("📢 Send the message you want to broadcast to all users:")
    return ASK_MESSAGE

async def do_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    stats = get_stats()
    users = stats["users"]

    success = 0
    failed = 0

    await update.message.reply_text(f"📤 Broadcasting to {len(users)} users...")

    for user_id in users:
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=message_text,
                parse_mode=ParseMode.HTML
            )
            success += 1
        except Exception as e:
            logger.warning(f"❌ Failed to send message to {user_id}: {e}")
            failed += 1

    await update.message.reply_text(
        f"✅ Broadcast complete.\n\n"
        f"👥 Sent to: {success}\n"
        f"❌ Failed: {failed}"
    )
    return ConversationHandler.END

async def cancel_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Broadcast cancelled.")
    return ConversationHandler.END
