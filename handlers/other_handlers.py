import asyncio

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from module.data_base import get_list_user

import logging

router = Router()





@router.callback_query()
async def all_calback(callback: CallbackQuery) -> None:
    logging.info(f'all_calback: {callback.message.chat.id}')
    # print(callback.data)


@router.message()
async def all_message(message: Message) -> None:
    logging.info(f'all_message')
    if message.photo:
        logging.info(f'all_message message.photo')
        # print(message.photo[-1].file_id)

    if message.sticker:
        logging.info(f'all_message message.sticker')
        # Получим ID Стикера
        # print(message.sticker.file_id)
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


