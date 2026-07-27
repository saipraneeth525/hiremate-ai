import os
import requests

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==========================================
# CONFIGURATION
# ==========================================

TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

BACKEND_URL = "http://127.0.0.1:8001/analyze"

JD_FOLDER = "uploads/jd"
RESUME_FOLDER = "uploads/resumes"

os.makedirs(JD_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)

# Stores the upload mode for each Telegram user
user_mode = {}

# ==========================================
# START
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
🤖 Welcome to HireMate AI

Commands:

/jd       Upload Job Description

/resume   Upload Resume(s)

After uploading files simply ask:

• Rank all candidates
• Compare candidates
• Generate interview questions
• Best candidate
• Missing skills
"""
    )

# ==========================================
# JD MODE
# ==========================================

async def jd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode[update.effective_user.id] = "jd"

    await update.message.reply_text(
        "📄 Please upload the Job Description PDF or DOCX."
    )

# ==========================================
# RESUME MODE
# ==========================================

async def resume(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_mode[update.effective_user.id] = "resume"

    await update.message.reply_text(
        "📁 Upload one or more resumes.\n\nSend them one by one."
    )

# ==========================================
# DOCUMENT HANDLER
# ==========================================

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in user_mode:
        await update.message.reply_text(
            "Use /jd or /resume before uploading files."
        )
        return

    document = update.message.document

    file = await context.bot.get_file(document.file_id)

    filename = document.file_name

    mode = user_mode[user_id]

    if mode == "jd":

        # Remove old JD
        for f in os.listdir(JD_FOLDER):
            os.remove(os.path.join(JD_FOLDER, f))

        save_path = os.path.join(JD_FOLDER, filename)

        await file.download_to_drive(save_path)

        await update.message.reply_text(
            f"✅ Job Description uploaded:\n{filename}"
        )

    elif mode == "resume":

        save_path = os.path.join(RESUME_FOLDER, filename)

        await file.download_to_drive(save_path)

        await update.message.reply_text(
            f"✅ Resume uploaded:\n{filename}"
        )

# ==========================================
# CHAT
# ==========================================

async def recruiter_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    question = update.message.text

    try:

        response = requests.post(
            BACKEND_URL,
            json={
                "question": question
            },
            timeout=180
        )

        result = response.json()

        answer = result.get("analysis", "No response received.")

        # Telegram limit
        for i in range(0, len(answer), 4000):
            await update.message.reply_text(answer[i:i+4000])

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error\n\n{str(e)}"
        )

# ==========================================
# MAIN
# ==========================================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("jd", jd))
app.add_handler(CommandHandler("resume", resume))

app.add_handler(
    MessageHandler(
        filters.Document.ALL,
        handle_document
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        recruiter_chat
    )
)

print("🤖 HireMate AI Telegram Bot Running...")

app.run_polling()