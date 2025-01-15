import logging
import os
import tempfile

from aiogram import Bot, Dispatcher, executor, types
from decouple import config

import crop_video

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
try:
    bot_token = config("BOT_TOKEN")
    bot = Bot(token=bot_token)
except:
    logging.error("Faltan las variables de entorno")
    exit()

dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        (
            "*English:* I am a bot, I can convert video messages in video notes.\n"
            "Send or forward me videos to convert them.\n"
            "Please use short videos.\n\n"
            "*Español:* Soy un bot, Puedo convertir videos en notas de video.\n"
            "Envíame o reenvíame videos para convertirlos.\n"
            "Por favor usa videos cortos."
        ),
        parse_mode="markdown",
    )


@dp.message_handler(content_types=["video"])
async def convert(message: types.Message):
    response = await message.answer("Processing...")
    with tempfile.NamedTemporaryFile(suffix='.mp4', dir=os.getcwd()) as video:
        await bot.download_file_by_id(message.video.file_id, video.name)
        with tempfile.NamedTemporaryFile(suffix='.mp4', dir=os.getcwd()) as out_video:
            size, duration = crop_video.video_crop(video.name, out_video.name)

            answer = await message.answer_video_note(
                video_note=out_video.read(), duration=duration
            )
            if not answer:
                await response.edit_text("I can't convert this video, sorry :'(")
            else:
                await response.delete()


if __name__ == '__main__':
    logging.info("Bot Running...")
    try:
        executor.start_polling(dp, skip_updates=True)
    finally:
        logging.info("Bot off")
