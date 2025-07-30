import telebot
from flask import Flask, request

# توکن ربات و آیدی کانال VIP شما
TOKEN = "8134095691:AAFZNQEvKexhDVcgupYzXdgrJwmSI53S7dQ"
CHANNEL_ID = "@vipdownloadclub"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot is running'

@app.route(f"/{TOKEN}", methods=['POST'])
def receive_update():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK', 200

# دریافت فایل از کاربر (ویدیو، فایل، صوت)
@bot.message_handler(content_types=['document', 'video', 'audio'])
def handle_file(message):
    try:
        user_id = message.from_user.id
        status = bot.get_chat_member(CHANNEL_ID, user_id).status

        if status in ['member', 'administrator', 'creator']:
            file = message.document or message.video or message.audio
            file_info = bot.get_file(file.file_id)
            download_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
            bot.reply_to(message, f"✅ لینک مستقیم دانلود:\n{download_url}")
        else:
            bot.reply_to(message, f"⛔️ برای دریافت لینک، ابتدا در کانال عضو شوید:\n{CHANNEL_ID}")

    except Exception as e:
        bot.reply_to(message, f"❌ خطا:\n{e}")

# تست ساده: اگر هیچ کدام از بالا نبود، این فعال می‌شود
@bot.message_handler(func=lambda message: True)
def echo_test(message):
    bot.reply_to(message, "✅ ربات فعاله، ولی منتظر فایل هستم.")

if __name__ == "__main__":
    app.run()
