from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from utils.stats import get_stats
from utils.admin_IDs import is_admin
from database.db import get_user_count, get_upload_count, get_total_storage_used  # You can create these if needed


ADMINS = set()

ADMIN_IDS = [1615680044, 5621290261, 5765156518]  # You can add more admin user IDs

# Commands available to everyone
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ For any query Please join our universal channel @shadowStreamer.")

# Admin-only commands
# ✅ generate_link
async def generate_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
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
 user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("🚫 You are not authorized to view stats.")
        return

    user_count = await get_user_count()
    upload_count = await get_upload_count()
    storage_used = await get_total_storage_used()

    text = (
        "📊 <b>Bot Statistics</b>\n\n"
        f"👥 <b>Users:</b> {user_count}\n"
        f"📁 <b>Files Uploaded:</b> {upload_count}\n"
        f"💾 <b>Total Storage Used:</b> {storage_used}"
    )

    await update.message.reply_text(text, parse_mode=ParseMode.HTML)

# ✅ User Details
async def show_user_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Fetching user details...")
# ✅ Broadcast
async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📣 Broadcasting your message...")




WAITING_FOR_BROADCAST = 1

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("🚫 You are not authorized to broadcast.")
        return ConversationHandler.END

    await update.message.reply_text(
        "📣 Please send the message you want to broadcast to all users.",
        reply_markup=ReplyKeyboardRemove()
    )
    return WAITING_FOR_BROADCAST

async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database.db import get_all_user_ids  # implement this if you haven't
    message = update.message
    user_ids = await get_all_user_ids()
    success = 0
    fail = 0

    for user_id in user_ids:
        try:
            await context.bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat_id,
                message_id=message.message_id
            )
            success += 1
        except:
            fail += 1

    await update.message.reply_text(
        f"✅ Broadcast completed.\n\n📤 Sent: {success}\n❌ Failed: {fail}"
    )
    return ConversationHandler.END

async def cancel_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Broadcast canceled.")
    return ConversationHandler.END



def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024.0



