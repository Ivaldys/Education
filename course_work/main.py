import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config_data.config import load_config
from environs import Env
import handlers



# Функция конфигурирования и запуска бота
async def main():
    #Загружаем конфиг
    config = load_config()
    storage = MemoryStorage()

    # Создаем объекты бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(handlers.user_handlers.router)
    dp.include_router(handlers.teacher_handlers.router)
    dp.include_router(handlers.client_handlers.router)
    dp.include_router(handlers.other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())