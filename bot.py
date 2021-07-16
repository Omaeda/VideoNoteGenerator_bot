import logging
import os

import crop_video
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'BOT TOKEN HERE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
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
    crop_video.crop(f"file_{user_id}.mp4", f"new_file_{user_id}.mp4")
    with open(f"new_file_{user_id}.mp4", "rb") as file:
        await message.answer_video_note(file)
    try:
        os.remove(f"file_{user_id}.mp4")
        os.remove(f"new_file_{user_id}.mp4")
    except Exception:
        pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
