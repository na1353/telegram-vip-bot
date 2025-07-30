import os
import telebot
from flask import Flask, request, send_file

TOKEN = "8134095691:AAFZNQEvKexhDVcgupYzXdgrJwmSI53S7dQ"
CHANNEL_USERNAME = "vipdownloadclub"
BASE_URL = "https://telegram-vip-bot-gqv5.onrender.com/"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def is_user_member(user_id):
    try:
        status = bot.get_chat_member("@" + CHANNEL_USERNAME, user_id).status
        return status in ["member", "administrator", "creator"]
    except:
        return False

@bot.message_handler(content_types=["document"])
def handle_files(message):
    user_id = message.from_user.id
    if not is_user_member(user_id):
        bot.send_message(user_id, f"⛔️ برای استفاده از ربات، عضو کانال شوید:\nhttps://t.me/{CHANNEL_USERNAME}")
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = os.path.join(DOWNLOAD_FOLDER, message.document.file_name)

    with open(file_path, 'wb') as f:
        f.write(downloaded_file)

    file_url = BASE_URL + "file/" + message.document.file_name
    bot.send_message(user_id, f"✅ فایل با موفقیت ذخیره شد.\n📥 لینک مستقیم:\n{file_url}")

@app.route("/file/<filename>")
def serve_file(filename):
    path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return "❌ فایل یافت نشد.", 404

@app.route("/8134095691:AAFZNQEvKexhDVcgupYzXdgrJwmSI53S7dQ", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route("/")
def index():
    return "✅ Bot is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
