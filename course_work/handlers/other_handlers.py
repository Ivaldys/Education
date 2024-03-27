from aiogram import  Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from config_data.config import load_config

router = Router()
config = load_config()

bot = Bot(token=config.tg_bot.token)


@router.callback_query(F.data == 'button_client_pressed')
async def process_button_client_press(callback: CallbackQuery):
    await bot.edit_message_media()
    await callback.answer(text='Ура! Вы ученик!')


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@router.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)
