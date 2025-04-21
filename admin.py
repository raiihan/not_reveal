from telegram import Update
from telegram.ext import ContextTypes

ADMINS = set()

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        admin_id = int(context.args[0])
        ADMINS.add(admin_id)
        await update.message.reply_text(f"✅ Admin {admin_id} added.")
    else:
        await update.message.reply_text("❗ Usage: /addadmin <user_id>")

async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        admin_id = int(context.args[0])
        ADMINS.discard(admin_id)
        await update.message.reply_text(f"❌ Admin {admin_id} removed.")
    else:
        await update.message.reply_text("❗ Usage: /removeadmin <user_id>")

async def list_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMINS:
        admins = "\n".join(map(str, ADMINS))
        await update.message.reply_text(f"👤 Current Admins:\n{admins}")
    else:
        await update.message.reply_text("⚠️ No admins found.")