import logging
import tempfile
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
    await message.reply(("I am a bot, I can convert video messages in video notes.\n\n"
                         "Please use short videos"))


@dp.message_handler(content_types=["video"])
async def convert(message: types.Message):
    response = await message.answer("Processing...")
    with tempfile.NamedTemporaryFile(suffix='.mp4', dir=os.getcwd()) as video:
        await bot.download_file_by_id(message.video.file_id, video.name)
        with tempfile.NamedTemporaryFile(suffix='.mp4', dir=os.getcwd()) as out_video:
            size, duration = crop_video.video_crop(video.name, out_video.name)

            answer = await message.answer_video_note(
                video_note=out_video.read(),
                duration=duration
            )
            if not answer:
                await response.edit_text("I can't convert this video, sorry :'(")
            else:
                await response.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
