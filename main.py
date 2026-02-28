import asyncio
import logging

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

# ---------- Хендлер для новых постов канала в группе обсуждений ----------
@dp.message(
    F.chat.type == ChatType.SUPERGROUP,
    F.sender_chat != None,
    F.is_automatic_forward == True
)
async def auto_comment(message: Message):
    """Автоматически отправляет картинку с кнопками как комментарий"""
    try:
        photo = FSInputFile(IMAGE_PATH)

        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            reply_to_message_id=message.message_id,
            reply_markup=build_keyboard()
        )

        logger.info(f"✅ Комментарий отправлен для сообщения {message.message_id}")

    except Exception as e:
        logger.error(f"❌ Ошибка при отправке комментария: {e}")

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