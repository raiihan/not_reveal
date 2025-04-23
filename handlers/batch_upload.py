from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

WAITING_FILES = range(1)

# Start batch upload process
async def start_batch_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["batch_links"] = []
    await update.message.reply_text("📤 Send multiple files one by one. Type /done when finished.")
    return WAITING_FILES

# Handle each uploaded file
async def handle_uploaded_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio
    if not file:
        await update.message.reply_text("❗ Only document/video/audio files are supported.")
        return

    # Forward to private channel
    channel_id = -1002282914539  # Store Room channel
    sent = await context.bot.forward_message(chat_id=channel_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)

    # Generate deep link from message_id
    msg_id = sent.message_id
    deep_link = f"https://t.me/NotRevealBot?start={msg_id}"
    context.user_data["batch_links"].append(deep_link)

    await update.message.reply_text(f"✅ Uploaded. Link: {deep_link}")

# Finish batch
async def done_batch_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    links = context.user_data.get("batch_links", [])
    if not links:
        await update.message.reply_text("⚠️ No files uploaded.")
    else:
        await update.message.reply_text("✅ Batch upload complete:\n" + "\n".join(links))
    return ConversationHandler.END
