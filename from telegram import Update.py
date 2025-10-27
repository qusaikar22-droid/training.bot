from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime

# Replace with your actual Telegram bot token
BOT_TOKEN = "7656913696:AAFF_l13O8FS5kAvnj9ZN_SSL7_HUqYfNjg"

LOG_FILE = "workouts.txt"
REMINDER_TIME = "15:00"  # default time (you can change it)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yo Qusai 💪 Your training bot is online!\nUse /trained to log a workout or /progress to check your history.")

async def trained(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = ' '.join(context.args)
    if not user_input:
        await update.message.reply_text("Please include your workout info.\nExample: /trained Push 12.5x10 OHP 12x8 Diamond 10x3")
        return
    
    log_entry = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} - {user_input}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    await update.message.reply_text(f"✅ Logged: {user_input}")

async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-5:]
        if not lines:
            await update.message.reply_text("No logs yet. Use /trained to log your first session.")
            return
        await update.message.reply_text("📊 Last workouts:\n" + ''.join(lines))
    except FileNotFoundError:
        await update.message.reply_text("No logs found yet.")
        
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trained", trained))
app.add_handler(CommandHandler("progress", progress))

print("Bot running...")
app.run_polling()
