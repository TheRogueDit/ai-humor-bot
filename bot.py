import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# === НАСТРОЙКИ ===
BOT_TOKEN = "8307843956:AAF13N0wPXv9OZr6WCgFTVFWAYZ-0LBhUSc"
CHANNEL_ID = "@IIHumorFuture"
ALLOWED_USER_ID = 684685584  # твой ID

logging.basicConfig(level=logging.INFO)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ALLOWED_USER_ID:
        await update.message.reply_text("🚫 У вас нет доступа.")
        return

    video = update.message.video
    document = update.message.document

    if not (video or (document and document.mime_type and document.mime_type.startswith('video'))):
        await update.message.reply_text("Пожалуйста, отправьте видео.")
        return

    # Подпись с ссылкой на канал
    caption = "Создано с помощью [ИИ 🤖](https://t.me/IIHumorFuture)"

    try:
        if video:
            await context.bot.send_video(
                chat_id=CHANNEL_ID,
                video=video.file_id,
                caption=caption,
                parse_mode="Markdown"
            )
        else:
            await context.bot.send_document(
                chat_id=CHANNEL_ID,
                document=document.file_id,
                caption=caption,
                parse_mode="Markdown"
            )
        await update.message.reply_text("✅ Видео опубликовано в канале!")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text(f"❌ Ошибка публикации: {str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, handle_video))
    logging.info("Бот запущен. Жду видео...")
    app.run_polling()

if __name__ == "__main__":
    main()