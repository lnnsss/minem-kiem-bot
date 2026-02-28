import asyncio
import logging
import json
from asyncio import sleep

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.enums import ChatType

from config import BOT_TOKEN, IMAGE_PATH, BUTTONS

# ---------- Настройка логирования ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Инициализация бота и диспетчера ----------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ---------- Функция для клавиатуры с кнопками ----------
def build_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=btn["text"], url=btn["url"])]
        for btn in BUTTONS
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# ---------- Функция отправки фото с повторными попытками ----------
async def send_photo_retry(chat_id, photo, reply_to_message_id, reply_markup, retries=3):
    for attempt in range(retries):
        try:
            await bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup,
                timeout=120  # увеличенный таймаут
            )
            logger.info(f"✅ Комментарий отправлен для сообщения {reply_to_message_id}")
            return
        except Exception as e:
            logger.warning(f"Попытка {attempt+1} не удалась: {e}")
            await sleep(3)
    logger.error(f"❌ Не удалось отправить фото после {retries} попыток для сообщения {reply_to_message_id}")

# ---------- Хендлер для новых постов канала в группе обсуждений ----------
@dp.message(
    F.chat.type == ChatType.SUPERGROUP,
    F.sender_chat != None,
    F.is_automatic_forward == True
)
async def auto_comment(message: Message):
    """Автоматически отправляет картинку с кнопками как комментарий"""
    photo = FSInputFile(IMAGE_PATH)
    await send_photo_retry(
        chat_id=message.chat.id,
        photo=photo,
        reply_to_message_id=message.message_id,
        reply_markup=build_keyboard()
    )

# ---------- Для теста: лог всех апдейтов ----------
# (можно закомментировать после отладки)
@dp.message()
async def debug_all(message: Message):
    logger.debug(f"DEBUG: Новое сообщение {message.message_id}, chat_id={message.chat.id}, sender_chat={getattr(message.sender_chat, 'title', None)}")

# ---------- Основная функция запуска ----------
async def main():
    logger.info("🚀 Бот запущен. Начинаем polling...")
    # timeout=60 -> long polling 60 сек
    # relax=3 -> пауза 3 сек после ошибки
    await dp.start_polling(bot, timeout=60, relax=3, allowed_updates=None)

# ---------- Точка входа ----------
if __name__ == "__main__":
    asyncio.run(main())