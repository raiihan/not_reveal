from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext
import logging
import os
from telegram import Update

app = FastAPI()

# Set up logging
logger = logging.getLogger(__name__)

# Replace this with your bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Set up the Telegram application with your token
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Admin check function
def is_admin(user_id):
    return user_id == OWNER_ID

# Function to handle file uploads
async def handle_file_upload(update: Update, context: CallbackContext):
    if is_admin(update.effective_user.id):
        file = update.message.document
        if file:
            file_id = file.file_id
            file_name = file.file_name
            file_size = file.file_size

            # Upload the file to the private channel
            await context.bot.send_document(chat_id=CHANNEL_ID, document=file_id)

            # Send the deep link message
            deep_link = f"https://t.me/{context.bot.username}?start={file_id}"
            await update.message.reply_text(
                f"✅ File uploaded!\nName: {file_name}\nSize: {file_size} bytes\n\n"
                f"Click the link to get your file: {deep_link}"
            )
        else:
            await update.message.reply_text("❌ No file received.")
    else:
        await update.message.reply_text("❌ You are not authorized to upload files.")

# Webhook endpoint for Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        # Parse the incoming JSON data from Telegram
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)

        # Call the file upload handler
        await handle_file_upload(update, telegram_app)
        await telegram_app.process_update(update)
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
