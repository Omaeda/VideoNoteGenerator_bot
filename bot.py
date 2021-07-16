import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from decouple import config

import crop_video

try:
    bot_token = config("BOT_TOKEN")
    bot = Bot(token=bot_token)
except:
    logging.error("Faltan las variables de entorno")
    exit()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher

dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(content_types=["video"])
async def convert(message: types.Message):
    user_id = message.from_user.id
    with open(f"file_{user_id}.mp4", "wb") as f:
        await bot.download_file_by_id(message.video.file_id, f)
    size, duration = crop_video.video_crop(f"file_{user_id}.mp4", f"new_file_{user_id}.mp4")
    with open(f"new_file_{user_id}.mp4", "rb") as file:
        await message.answer_video_note(
            video_note=file,
            duration=duration,
            length=size
        )
    try:
        os.remove(f"file_{user_id}.mp4")
        os.remove(f"new_file_{user_id}.mp4")
    except Exception:
        pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
