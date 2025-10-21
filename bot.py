import os
import logging
import urllib.request
import urllib.parse
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN", "8307843956:AAF13N0wPXv9OZr6WCgFTVFWAYZ-0LBhUSc")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@IIHumorFuture")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "684685584"))
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

logging.basicConfig(level=logging.INFO)

def generate_ai_caption():
    if not DEEPINFRA_API_KEY:
        return "ИИ сегодня отдыхает 😴"
    try:
        url = "https://api.deepinfra.com/v1/openai/chat/completions"
        data = {
            "model": "meta-llama/Meta-Llama-3-8B-Instruct",
            "messages": [
                {"role": "system", "content": "Ты — автор канала о видео от ИИ. Пиши короткие, смешные подписи на русском. Без хештегов."},
                {"role": "user", "content": "Напиши подпись к новому видео."}
            ],
            "max_tokens": 80,
            "temperature": 0.9
        }
        headers = {
            "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
            "Content-Type": "application/json"
        }

        # Создаём запрос через urllib
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return "Новое видео от будущего! 🤖"

async def make_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 Не твоё!")
        return
    await update.message.reply_text("🧠 Думаю...")
    caption = generate_ai_caption()
    full_text = f"{caption}\nСоздано с помощью [ИИ 🤖](https://t.me/IIHumorFuture)"
    await context.bot.send_message(chat_id=CHANNEL_ID, text=full_text, parse_mode="Markdown")
    await update.message.reply_text("✅ Готово!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("makevideo", make_video))
    app.run_polling()

if __name__ == "__main__":
    main()
