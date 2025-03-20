import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openai

# Завантаження змінних середовища
TOKEN = os.getenv("BOT_TOKEN")  # Токен Telegram-бота
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # API-ключ OpenAI

# Налаштування логування (щоб бачити помилки в Render)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ініціалізація OpenAI API
openai.api_key = OPENAI_API_KEY

# Функція для обробки команд /start
async def start(update: Update, context):
    await update.message.reply_text("Привіт! Я бот Lila. Напиши мені щось, і я відповім.")

# Функція для обробки текстових повідомлень і запитів до OpenAI
async def chat(update: Update, context):
    user_message = update.message.text  # Отримуємо повідомлення від користувача
    logging.info(f"User message: {user_message}")  # Логуємо повідомлення

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Використовуємо найшвидшу модель GPT-4o
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response["choices"][0]["message"]["content"]  # Отримуємо відповідь від OpenAI
    except Exception as e:
        reply = f"Помилка API: {e}"  # Відправляємо повідомлення про помилку користувачу
        logging.error(f"OpenAI API Error: {e}")

    await update.message.reply_text(reply)  # Відправляємо відповідь у Telegram

# Основна функція запуску бота
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()