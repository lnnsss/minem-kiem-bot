import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден в .env")

IMAGE_PATH = "image.jpg"

BUTTONS = [
    {
        "text": "Магазин",
        "url": "https://minem-kiem.ru/shop"
    },
    {
        "text": "Вконтакте",
        "url": "https://vk.com/minem.kiem"
    },
    {
        "text": "Поддержка",
        "url": "https://t.me/minemmanager"
    }
]