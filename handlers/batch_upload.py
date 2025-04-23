from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    ConversationHandler
)

# Admin check function
def is_admin(user_id):
    return user_id in [1615680044, 5621290261, 5765156518]  # Replace with actual admin user IDs

# Function to convert file size into a human-readable format
def human_readable_size(size: int):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 ** 3:
        return f"{size / 1024**2:.2f} MB"
    else:
        return f"{size / 1024**3:.2f} GB"

# Starting batch upload
WAITING_FOR_FILES = 1

async def start_batch_upload(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text(
            "🚫 You are not authorized to use this command."
        )
        return ConversationHandler.END

    # Initialize user_data to store batch files
    context.user_data['batch_files'] = []
    
    await update.message.reply_text(
        "📤 Send the files one by one. When you're done, send /done to finish the batch upload."
    )
    return WAITING_FOR_FILES

# Handling file uploads for batch upload (without filters)
async def handle_file_upload(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text(
            "🚫 Sorry, only bot admins can upload files.\n"
            "✨ This feature is for secure content delivery only."
        )
        return

    message = update.message
    bot = context.bot

    # Check if the message contains a document, video, or photo
    file = None
    file_type = "Unknown"
    file_name = "Unknown"
    file_size = "Unknown"
    
    # Check for Document
    if message.document:
        file = message.document
        file_name = file.file_name
        file_size = human_readable_size(file.file_size)
        file_type = "Document"
    
    # Check for Video
    elif message.video:
        file = message.video
        file_name = file.file_name or "Unnamed Video"
        file_size = human_readable_size(file.file_size)
        file_type = "Video"
    
    # Check for Photo
    elif message.photo:
        file = message.photo[-1]  # Get the last photo in case multiple sizes are present
        file_name = "Photo.jpg"
        file_size = human_readable_size(file.file_size)
        file_type = "Photo"
    
    if file:
        # Copy message to the channel (to keep it clean)
        sent = await bot.copy_message(
            chat_id=CHANNEL_ID,  # Replace with your channel ID
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )

        # Store the file ID in user data for batch processing
        context.user_data['batch_files'].append(sent.message_id)

        # Send confirmation message
        await update.message.reply_text(f"✅ Received {file_type}: {file_name} ({file_size})")

    else:
        await update.message.reply_text("❗ That doesn't seem to be a valid file. Please send a document/video/audio.")

    return WAITING_FOR_FILES

# Completing the batch upload and sending deep links for all uploaded files
async def complete_batch_upload(update: Update, context: CallbackContext):
    files = context.user_data.get('batch_files', [])
    if not files:
        await update.message.reply_text("⚠️ No files received.")
    else:
        links = [
            f"{idx + 1}. 🔗 https://t.me/{context.bot.username}?start={file_id}"
            for idx, file_id in enumerate(files)
        ]
        await update.message.reply_text("✅ Batch upload complete:\n" + "\n".join(links))

    context.user_data.clear()  # Clear stored data
    return ConversationHandler.END

# Cancel batch upload
async def cancel_batch_upload(update: Update, context: CallbackContext):
    await update.message.reply_text("❌ Batch upload canceled.")
    return ConversationHandler.END

# Batch upload handler setup
def get_batch_upload_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('batchupload', start_batch_upload)],
        states={
            WAITING_FOR_FILES: [
                MessageHandler(
                    lambda message: (
                        message.document or message.video or (message.photo and message.photo[-1])
                    ),
                    handle_file_upload
                ),
                CommandHandler('done', complete_batch_upload),
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel_batch_upload)],
    )
