from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    MessageHandler,
    filters,
    CommandHandler,
    ContextTypes
)

import logging
import os
import math
from telegram import Update

app = FastAPI()

# Initialize Telegram Application (Corrected)
telegram_app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()  # Initialize Application

# Set up logging
logger = logging.getLogger(__name__)

# Replace this with your bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMINS = [OWNER_ID, 5621290261, 5765156518]  # Replace with your actual admin Telegram IDs

# Set up the Telegram application with your token
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Admin check function
def is_admin(user_id):
    return user_id == OWNER_ID

ADMINS = [OWNER_ID, 123456789, 987654321]  # Replace with your actual admin Telegram IDs

def is_admin(user_id):
    return user_id in ADMINS

async def admin_list(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
    admin_list_text = "\n".join([f"👤 `{admin}`" for admin in ADMINS])
    await update.message.reply_text(f"🔐 Current Admins:\n{admin_list_text}", parse_mode="Markdown")



async def start(update: Update, context: CallbackContext):
    try:
        args = context.args
        user_id = update.effective_user.id

        # 💬 Custom welcome messages based on admin role
        if not args:
            if is_admin(user_id):
                await update.message.reply_text(
                    "👋 Welcome, Admin!\n\nUse the menu to upload files and manage the bot.\n\nCommands:\n"
                    "- /adminlist\n- Upload any file to generate a deep link\n\nExample Link:\n"
                    f"https://t.me/{context.bot.username}?start=123"
                )
            else:
                await update.message.reply_text(
                    "👋 Welcome!\n\nThis bot allows you to download files using deep links.\n"
                    "Ask the admin for a download link.\n\nExample:\n"
                    f"https://t.me/{context.bot.username}?start=123"
                )
            return

        # 🧩 If /start has a deep link argument — fetch file
        msg_id = int(args[0])

        # ⏳ Send a fancy loading message
        loader = await update.message.reply_text("🔍 Retrieving your file... Please wait.")

        # 📤 Copy file from private channel to user
        sent = await context.bot.copy_message(
            chat_id=user_id,
            from_chat_id=CHANNEL_ID,
            message_id=msg_id
        )

        # 🧹 Delete loader
        await loader.delete()


    except Exception as e:
        logger.error(f"❌ Error in /start handler: {e}")
        await update.message.reply_text("❌ File not found or removed. The link may be broken. Please check again!")

# Helper to format bytes to human-readable size
def human_readable_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    return f"{round(size_bytes / p, 2)} {size_name[i]}"



# Function to handle file uploads
# Define the handler to process file 
    
    # Function to handle file uploads with admin check
# Function to handle file uploads with admin check
async def handle_file_upload(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id
        if not is_admin(user_id):
            await update.message.reply_text("🚫 Only admins can upload files.")
            return
        message = update.message
        bot = context.bot

        file = message.document or message.video or (message.photo[-1] if message.photo else None)

        # Default values
        file_name = "Unknown"
        file_size = "Unknown"
        file_type = "Unknown"

        # Detect file type and extract info
        if message.document:
            file_name = message.document.file_name
            file_size = human_readable_size(message.document.file_size)
            file_type = "Document"
        elif message.video:
            file_name = message.video.file_name or "Unnamed Video"
            file_size = human_readable_size(message.video.file_size)
            file_type = "Video"
        elif message.photo:
            file_name = "Photo.jpg"
            file_size = human_readable_size(message.photo[-1].file_size)
            file_type = "Photo"

        # ✅ Forward the file to private channel
        sent = await bot.forward_message(
            chat_id=CHANNEL_ID,
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )

        # ✅ Create deep link using forwarded message ID
        deep_link = f"https://t.me/{bot.username}?start={sent.message_id}"

        # ✅ Send formatted response to user
        response_text = f"""✅ File Uploaded!

📁 Name: `{file_name}`
📦 Size: `{file_size}`
📂 Type: `{file_type}`

🔗 Access anytime:
{deep_link}
"""

        await message.reply_text(response_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ Error handling file: {e}")
        await update.message.reply_text("⚠️ Oops! We hit a snag while uploading. Please try again❌.")



# Add the file upload handler to the application
telegram_app.add_handler(CommandHandler("adminlist", admin_list))
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO, handle_file_upload))


@app.on_event("startup")
async def startup():
    logger.info("✅ Telegram bot initialized")
    await telegram_app.initialize()  # Properly await initialization

# Webhook endpoint for Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()  # Get incoming data from Telegram
        update = Update.de_json(data, telegram_app.bot)  # Convert to Update object
        
        # Process the update with the properly initialized application
        await telegram_app.process_update(update)  # This will now also process file uploads
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
