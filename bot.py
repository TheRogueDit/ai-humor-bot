import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === НАСТРОЙКИ ===
BOT_TOKEN = os.getenv("BOT_TOKEN", "8307843956:AAF13N0wPXv9OZr6WCgFTVFWAYZ-0LBhUSc")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@IIHumorFuture")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "684685584"))
DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

logging.basicConfig(level=logging.INFO)

# --- Генерация подписи через DeepInfra (Llama 3) ---
def generate_ai_caption():
    if not DEEPINFRA_API_KEY:
        return "Новое видео от будущего! 🤖"

    url = "https://api.deepinfra.com/v1/openai/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPINFRA_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {"role": "system", "content": "Ты — автор Telegram-канала о видео, созданных ИИ. Пиши короткие, смешные, цепляющие подписи на русском языке. Без хештегов."},
            {"role": "user", "content": "Напиши подпись к новому ИИ-видео."}
        ],
        "max_tokens": 80,
        "temperature": 0.85
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logging.error(f"Ошибка DeepInfra: {e}")
        return "ИИ сегодня в ударе! 🤖"

# --- Заглушка для видео (пока без генерации) ---
def generate_ai_video():
    # Позже заменим на Replicate/Kaiber
    return None  # временно не генерируем видео

# --- Команда /makevideo ---
async def make_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 Доступ запрещён.")
        return

    await update.message.reply_text("🧠 Генерирую ИИ-подпись...")

    caption_text = generate_ai_caption()
    full_caption = f"{caption_text}\n\nСоздано с помощью [ИИ 🤖](https://t.me/IIHumorFuture)"

    # Пока публикуем ТОЛЬКО подпись (без видео)
    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=full_caption,
            parse_mode="Markdown"
        )
        await update.message.reply_text("✅ Подпись опубликована! (Видео — в будущем)")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")

# --- Основной запуск ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("makevideo", make_video))
    logging.info("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()