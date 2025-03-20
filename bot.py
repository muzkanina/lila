import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openai

# Завантаження змінних середовища
TOKEN = os.getenv("7573113232:AAHOzjVBx0Ym4bGcXGVn_XkrYP-jsn0fM7U")  # Токен Telegram-бота
OPENAI_API_KEY = os.getenv("***REMOVED***proj-dQbKQl5zeNawJoJVBthqzq5Q5yl-UJRvFh-roGCwx0ipcHn2VkGaqEp-aZq0PyMck2_KvaCqjoT3BlbkFJFWNC4WJolFIfSzXf8Jqam_nVOeyoRteiw9P5QwLAENVAdDEoHv1FYqajEcxU6R0plpJVazqzMA")  # API-ключ OpenAI

# Налаштування логування
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ініціалізація OpenAI
openai.api_key = OPENAI_API_KEY

# Функція для відповіді на повідомлення
async def chat(update: Update, context):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
    reply = response["choices"][0]["message"]["content"]
    await update.message.reply_text(reply)

# Функція для стартової команди
async def start(update: Update, context):
    await update.message.reply_text("Привіт! Я бот Lila. Напиши мені щось, і я відповім.")

# Основна функція
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()