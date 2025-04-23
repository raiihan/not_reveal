from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)

# ✅ Admin user IDs
ADMINS = [1615680044, 5621290261, 5765156518]

# ✅ Conversation state
WAITING_FOR_FILES = 1

# ✅ Check if user is admin
def is_admin(user_id):
    return user_id in ADMINS

# ✅ Start batch upload command
async def start_batch_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return ConversationHandler.END

    context.user_data['batch_files'] = []
    await update.message.reply_text(
        "📤 Send the files one by one. When you're done, send /done to finish the batch upload."
    )
    return WAITING_FOR_FILES

# ✅ Handle each file sent by the admin
async def handle_file_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio
    if file:
        context.user_data['batch_files'].append(file.file_id)
        await update.message.reply_text(f"✅ Received: {file.file_name or file.mime_type}")
    else:
        await update.message.reply_text("❗ That doesn't seem to be a valid file. Please send a document, video, or audio.")
    return WAITING_FOR_FILES

# ✅ Complete the batch upload
async def complete_batch_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = context.user_data.get('batch_files', [])
    if not files:
        await update.message.reply_text("⚠️ No files received.")
    else:
        links = [
            f"{idx + 1}. 🔗 https://t.me/{context.bot.username}?start={file_id}"
            for idx, file_id in enumerate(files)
        ]
        await update.message.reply_text("✅ Batch upload complete:\n" + "\n".join(links))
    context.user_data.clear()
    return ConversationHandler.END

# ✅ Cancel the batch upload
async def cancel_batch_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Batch upload canceled.")
    return ConversationHandler.END

# ✅ Main conversation handler using correct PTB v20 filters
def get_batch_upload_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('batchupload', start_batch_upload)],
        states={
            WAITING_FOR_FILES: [
                MessageHandler(
                    filters.Document.ALL | filters.Video.ALL | filters.Audio.ALL,
                    handle_file_upload
                ),
                CommandHandler('done', complete_batch_upload),
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel_batch_upload)],
    )
