import asyncio

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from module.data_base import get_list_user, get_list_last_raffle
from services.get_exel import list_users_to_exel
from config_data.config import Config, load_config
import logging

router = Router()
config: Config = load_config()




@router.callback_query()
async def all_calback(callback: CallbackQuery) -> None:
    logging.info(f'all_calback: {callback.message.chat.id}')
    # print(callback.data)


@router.message()
async def all_message(message: Message) -> None:
    logging.info(f'all_message')
    list_super_admin = list(map(int, config.tg_bot.admin_ids.split(',')))
    if message.chat.id in list_super_admin:
        logging.info(f'all_message-admin')

        if message.text == '/get_logfile':
            file_path = "py_log.log"
            await message.answer_document(FSInputFile(file_path))

        if message.text == '/get_dbfile':
            file_path = "database.db"
            await message.answer_document(FSInputFile(file_path))

        if message.text == '/get_listusers':
            list_user = get_list_user()
            text = 'Список пользователей:\n'
            for i, user in enumerate(list_user):
                text += f'{i+1}. {user[1]} - {user[2]}\n'
                if i % 10 == 0 and i > 0:
                    await asyncio.sleep(0.2)
                    await message.answer(text=text)
                    text = ''
            await message.answer(text=text)

        if message.text == '/get_exel':
            list_users_to_exel()
            file_path = "list_user.xlsx"  # или "folder/filename.ext"
            await message.answer_document(FSInputFile(file_path))

        if '/get_CULR' in message.text:
            logging.info(f'all_message-/get_CULR')
            list_message = message.text.split('_')
            if len(list_message) == 3:
                done_task = int(list_message[2])
                list_raffle = get_list_last_raffle(done_task=done_task)
                if list_raffle:
                    count_raffle_task = len(list_raffle)
                else:
                    count_raffle_task = 0
                list_raffle_0 = get_list_last_raffle(done_task=0)
                if list_raffle_0:
                    count_raffle_task_0 = len(list_raffle)
                else:
                    count_raffle_task_0 = 0
                await message.answer(text=f'Количество участников выполнивших {done_task} заданий: '
                                          f'{count_raffle_task}\n'
                                          f'Количество участников зарегистрировавшихся на участие в розыгрыше: '
                                          f'{count_raffle_task_0}')
            elif len(list_message) == 2:
                list_raffle = get_list_last_raffle(done_task=0)
                if list_raffle:
                    count_raffle_task = len(list_raffle)
                else:
                    count_raffle_task = 0
                await message.answer(text=f'Количество участников зарегистрировавшихся на участие в розыгрыше: '
                                          f'{count_raffle_task}')

