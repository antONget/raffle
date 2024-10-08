import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import handler_user, handler_admin, other_handlers, handler_raffle
from module.data_base import create_table_users, create_table_message_content
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.handler_raffle import get_task_monday, select_winer, send_new_raffle
# Инициализируем logger
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # create_table_users()
    # create_table_message_content()
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        filemode='w',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    # # понедельник
    scheduler.add_job(get_task_monday, 'cron', day_of_week=0, hour=13, minute=20, args=(0, bot,))
    # # вторник
    scheduler.add_job(get_task_monday, 'cron', day_of_week=1, hour=13, minute=20, args=(1, bot,))
    # # среда
    scheduler.add_job(get_task_monday, 'cron', day_of_week=2, hour=13, minute=20, args=(2, bot,))
    # # четверг
    scheduler.add_job(get_task_monday, 'cron', day_of_week=3, hour=13, minute=20, args=(3, bot,))
    # # пятница
    scheduler.add_job(get_task_monday, 'cron', day_of_week=4, hour=13, minute=20, args=(4, bot,))
    # # выбор победителей
    scheduler.add_job(select_winer, 'cron', day_of_week=5, hour=13, minute=20, args=(bot,))
    # воскресенье
    scheduler.add_job(send_new_raffle, 'cron', day_of_week=6, hour=15, minute=0, args=(bot,))
    # условно воскресенье рассылка о новом розыгрыше
    # scheduler.add_job(send_new_raffle, 'cron', minute=55, args=(bot,))
    # # условно понедельник
    # scheduler.add_job(get_task_monday, 'cron', minute=0, args=(0, bot,))
    # # условно вторник
    # scheduler.add_job(get_task_monday, 'cron', minute=10, args=(1, bot,))
    # # условно среда
    # scheduler.add_job(get_task_monday, 'cron', minute=20, args=(2, bot,))
    # # условно четверг
    # scheduler.add_job(get_task_monday, 'cron', minute=30, args=(3, bot,))
    # # условно пятница
    # scheduler.add_job(get_task_monday, 'cron', minute=40, args=(4, bot,))
    # # условно суббота выбор победителей
    # scheduler.add_job(select_winer, 'cron', minute=50, args=(bot,))
    # scheduler.add_job(get_task_monday, 'cron', day_of_week=0, minute=TEST_LIST_TIME[2], args=(0, bot,))
    # # вторник
    # scheduler.add_job(get_task_monday, 'cron', day_of_week=0, minute=TEST_LIST_TIME[3], args=(1, bot,))
    # # среда
    # scheduler.add_job(get_task_monday, 'cron', day_of_week=0, minute=TEST_LIST_TIME[4], args=(2, bot,))
    # # четверг
    # scheduler.add_job(get_task_monday, 'cron', day_of_week=0, minute=TEST_LIST_TIME[5], args=(3, bot,))
    # # пятница
    # scheduler.add_job(get_task_monday, 'cron', day_of_week=0, minute=TEST_LIST_TIME[6], args=(4, bot,))
    # # выбор победителей
    # scheduler.add_job(select_winer, 'cron', day_of_week=0, minute=TEST_LIST_TIME[6]+2, args=(bot,))
    scheduler.start()
    # Регистрируем router в диспетчере
    dp.include_router(handler_user.router)
    dp.include_router(handler_raffle.router)
    dp.include_router(handler_admin.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся update и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
