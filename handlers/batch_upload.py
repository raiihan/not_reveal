from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)

# Define state
WAITING_FOR_FILES = 1

# Start the batch upload
async def start_batch_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['batch_files'] = []
    await update.message.reply_text(
        "📤 Send the files one by one. When you're done, send /done to finish the batch upload."
    )
    return WAITING_FOR_FILES

# Handle individual file uploads
async def handle_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio
    if file:
        context.user_data['batch_files'].append(file.file_id)
        await update.message.reply_text(f"✅ Received: {file.file_name or file.mime_type}")
    else:
        await update.message.reply_text("❗ That doesn't seem to be a valid file. Please send a document/video/audio.")
    return WAITING_FOR_FILES

# Complete the batch upload
async def complete_batch_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = context.user_data.get('batch_files', [])
    if not files:
        await update.message.reply_text("⚠️ No files received.")
    else:
        links = []
        for idx, file_id in enumerate(files, start=1):
            links.append(f"{idx}. 🔗 https://t.me/{context.bot.username}?start={file_id}")
        await update.message.reply_text("✅ Batch upload complete:\n" + "\n".join(links))
    context.user_data.clear()
    return ConversationHandler.END

# Cancel handler (optional)
async def cancel_batch_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Batch upload canceled.")
    return ConversationHandler.END

# Add this in your main.py or bot.py to register the handler
def get_batch_upload_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('batchupload', start_batch_upload)],
        states={
            WAITING_FOR_FILES: [
                MessageHandler(filters.Document.ALL | filters.Video.ALL | filters.Audio.ALL, handle_file_upload),
                CommandHandler('done', complete_batch_upload)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel_batch_upload)],
    )
