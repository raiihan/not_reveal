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
import asyncio
import math
from keyboard_utils import get_user_keyboard, get_admin_keyboard, set_bot_commands
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.constants import ParseMode
from handlers.menu import show_menu
from handlers.admin_menu_actions import handle_admin_action
from handlers.admin import edit_file_description, get_upload_stats, batch_upload_files

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


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

admin_msg = (
    "👑 *Hello Admin!*\n\n"
    "Welcome to the NotRevealBot control panel.\n\n"
    "🔹 Use the menu to:\n"
    "• 📤 Upload files\n"
    "• 🔗 Generate deep links\n"
    "• 📊 View stats\n"
    "• 👥 Manage admins\n\n"
    "Let’s manage files in style!"
)

user_msg = (
    "👋 *Welcome to Connect Your Univers!*\n\n"
    "To get a file, just click on a secure button shared by admins like:\n"
    "`Enjoy your meal"
    "Enjoy safe download! 🚀"
)




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
        user_id = update.effective_user.id
        args = update.message.text.split()[1:] if update.message and update.message.text else []

        # 🧹 Delete the original /start message for clean chat
        try:
            await update.message.delete()
        except Exception as e:
            logger.warning(f"Failed to delete start command: {e}")

        # 💬 Send custom keyboard and welcome message
        if not args:
            keyboard = get_admin_keyboard() if is_admin(user_id) else get_user_keyboard()
            welcome_msg = admin_msg if is_admin(user_id) else user_msg

            # ✅ THIS ensures the custom keyboard shows in bottom-left
            await context.bot.send_message(
                chat_id=user_id,
                text=welcome_msg,
                reply_markup=keyboard
            )
            return

        # 🧩 Handle deep link argument
        try:
            msg_id = int(args[0])
        except (IndexError, ValueError):
            await context.bot.send_message(
                chat_id=user_id,
                text="⚠️ Invalid or broken link. Please ask the admin for a valid one.",
                reply_markup=get_admin_keyboard() if is_admin(user_id) else get_user_keyboard()  # Optional: Show keyboard here too
            )
            return

        # ⏳ Fancy loading message
        loading_msg = await context.bot.send_message(
            chat_id=user_id,
            text="⏳ Preparing your file 🔍, please wait..."
        )

        # 📤 Call helper function to handle file delivery and info
        await send_file_to_user(context, user_id, msg_id, "Unknown", "Unknown", "Unknown", loading_msg)

    except Exception as e:
        logger.error(f"❌ Error in /start handler: {e}")
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ File not found or removed. The link may be broken. Please check again!",
            reply_markup=get_admin_keyboard() if is_admin(user_id) else get_user_keyboard()
        )



# file delivery and info or send file to user function refactore
async def send_file_to_user(context, user_id, msg_id, file_name, file_type, file_size, loading_msg):
    try:
        # Try to send file
        sent = await context.bot.copy_message(
            chat_id=user_id,
            from_chat_id=CHANNEL_ID,
            message_id=msg_id
        )

        # Extract file info
        if sent.document:
            file_name = sent.document.file_name
            file_size = human_readable_size(sent.document.file_size)
            file_type = "Document"
        elif sent.video:
            file_name = sent.video.file_name or "Unnamed Video"
            file_size = human_readable_size(sent.video.file_size)
            file_type = "Video"
        elif sent.photo:
            file_name = "Photo.jpg"
            file_size = human_readable_size(sent.photo[-1].file_size)
            file_type = "Photo"

        # ✅ Delete the loading message right away
        try:
            await context.bot.delete_message(chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)
        except Exception as e:
            logger.warning(f"❌ Failed to delete loading message: {e}")

        # Send file info
        await context.bot.send_message(
            chat_id=user_id,
            text=f"📥 <b>{file_name}</b>\n📁 <i>{file_type} - {file_size}</i>",
            reply_to_message_id=sent.message_id,
            parse_mode=ParseMode.HTML
        )

      

    except Exception as e:
        logger.error(f"❌ Error copying or sending message: {e}")

        # Clean up loader only if it exists
        try:
            if loading_msg:
                await context.bot.delete_message(chat_id=loading_msg.chat.id, message_id=loading_msg.message_id)
        except Exception as e:
            logger.warning(f"❌ Failed to delete loader after error: {e}")

        # Don't send error if file already sent
        if 'sent' not in locals():
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ <b>Sorry! I couldn't retrieve the file.</b>",
                parse_mode=ParseMode.HTML
            )




# Helper to format bytes to human-readable size
def human_readable_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    return f"{round(size_bytes / p, 2)} {size_name[i]}"


# menu list is here

async def generate_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠 Generate Link feature is under construction.")

async def batch_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛠 Batch Upload feature is under construction.")

async def delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗑️ Send the file link or ID to delete.")

async def bot_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Bot Stats feature coming soon.")

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📢 Broadcast feature coming soon.")

async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🙍 User Info will be available soon.")
 

# menu handler

async def handle_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📤 Generate Link":
        await generate_link(update, context)
    elif text == "📂 Batch Upload":
        await batch_upload(update, context)
    elif text == "🗑️ Delete File":
        await delete_file(update, context)
    elif text == "📊 Bot Stats":
        await bot_stats(update, context)
    elif text == "📢 Broadcast":
        await broadcast_message(update, context)
    elif text == "🙍 User Info":
        await user_info(update, context)




# Function to handle file uploads
# Define the handler to process file 
    
    # Function to handle file uploads with admin check
# Function to handle file uploads with admin check
async def handle_file_upload(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id
        if not is_admin(user_id):
            await update.message.reply_text(
                "🚫 Sorry, only bot admins can upload files.\n"
                "✨ This feature is for secure content delivery only."
            )
            return

        message = update.message
        bot = context.bot
        file = message.document or message.video or (message.photo[-1] if message.photo else None)

        file_name = "Unknown"
        file_size = "Unknown"
        file_type = "Unknown"

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

        # ✅ Upload to channel using copy_message to keep it clean
        sent = await bot.copy_message(
            chat_id=CHANNEL_ID,
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )

        # ✅ Deep link with file ID
        deep_link = f"https://t.me/{bot.username}?start={sent.message_id}"

        # ✅ Styled Response
        text = f"""
✅ **File Uploaded Successfully!**

📁 **Name:** `{file_name}`
📦 **Size:** `{file_size}`
📂 **Type:** `{file_type}`

🔗 [Access this file anytime]({deep_link})
🔗 [{deep_link}]({deep_link})

"""
        await message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        logger.error(f"❌ Error uploading file: {e}")
        await update.message.reply_text("⚠️ Oops! Something went wrong while uploading the file.")


# Add the file upload handler to the application
# 🥇 First: Command handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("generatelink", generate_link))
telegram_app.add_handler(CommandHandler("batchupload", batch_upload))
telegram_app.add_handler(CommandHandler("deletefile", delete_file))
telegram_app.add_handler(CommandHandler("stats", bot_stats))
telegram_app.add_handler(CommandHandler("broadcast", broadcast_message))
telegram_app.add_handler(CommandHandler("userinfo", user_info))
telegram_app.add_handler(CommandHandler("adminlist", admin_list))
telegram_app.add_handler(CommandHandler("editfile", edit_file_description))
telegram_app.add_handler(CommandHandler("stats", get_upload_stats))
telegram_app.add_handler(CommandHandler("batch", batch_upload_files))

telegram_app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^(🚀 Start|↩️ Back)$'), show_menu))
telegram_app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^(🔗 Generate Link|📦 Batch Upload|👥 Admin List|🗑️ Delete File|📢 Broadcast|🧾 User Details|📊 Bot Stats)$'), handle_admin_action))


# 🥈 Second: File upload handler
telegram_app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO | filters.VIDEO, handle_file_upload))

# 🥉 Last: Menu text button handler
telegram_app.add_handler(MessageHandler(filters.TEXT, handle_menu_click))



@app.on_event("startup")
async def startup():
    logger.info("✅ Telegram bot initialized")
    await set_bot_commands(telegram_app)
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.bot.set_webhook("https://not-reveal.onrender.com/webhook")
    logger.info("🌐 Webhook set successfully")


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
