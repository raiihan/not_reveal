from telegram import Update
from telegram.ext import ContextTypes

from utils.admin_IDs import ADMINS

# Commands available to everyone
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ For any query Please join our universal channel @shadowStreamer.")

# Admin-only commands
# ✅ generate_link
async def generate_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        await update.message.reply_text("⛔ You are not authorized to use this command.")
        return
    await update.message.reply_text("🔗 Generating a deep link...")


# ✅ Edit File Description
async def edit_file_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❗ Usage: /editfile <file_id> <new_description>")
        return
    file_id = args[0]
    new_description = ' '.join(args[1:])
    # TODO: Update description in database or in-memory storage
    await update.message.reply_text(f"✅ Description for file `{file_id}` updated.")

# ✅ Batch Upload
async def batch_upload_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    documents = update.message.document
    if not documents:
        await update.message.reply_text("❗ Please upload files to batch upload.")
        return
    links = []
    for doc in documents:
        file_link = f"https://t.me/YourBot?start={doc.file_id}"
        links.append(file_link)
    await update.message.reply_text("✅ Files uploaded successfully:\n" + "\n".join(links))

async def delete_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗑️ Deleting file...")

# ✅ Admin List
async def list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMINS:
        admins = "\n".join(map(str, ADMINS))
        await update.message.reply_text(f"👤 Current Admins:\n{admins}")
    else:
        await update.message.reply_text("⚠️ No admins found.")


# ✅ Bot Stats
async def get_upload_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await update.message.reply_text("📣 Bot Stats ...")

# ✅ User Details
async def show_user_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Fetching user details...")
# ✅ Broadcast
async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📣 Broadcasting your message...")



