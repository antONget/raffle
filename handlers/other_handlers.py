import asyncio

from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from module.data_base import get_list_user, get_list_last_raffle, get_info_user
from services.get_exel import list_users_to_exel
from config_data.config import Config, load_config
from handlers.handler_raffle import send_new_raffle
import logging
import requests
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state
router = Router()
config: Config = load_config()


class Admin(StatesGroup):
    message_id = State()
    message_all = State()


def get_telegram_user(user_id, bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getChat'
    data = {'chat_id': user_id}
    response = requests.post(url, data=data)
    return response.json()


@router.callback_query()
async def all_calback(callback: CallbackQuery) -> None:
    logging.info(f'all_calback: {callback.message.chat.id}')
    # print(callback.data)


@router.message(StateFilter(Admin.message_id))
async def all_message(message: Message, bot: Bot, state: FSMContext) -> None:
    logging.info(f'Admin.message_id')
    message_id = message.html_text
    data = await state.get_data()
    id_user = int(data['id_user'])
    await bot.send_message(chat_id=id_user,
                           text=message_id)
    await message.answer(text='Сообщение отправлено')
    await state.set_state(default_state)


@router.message(StateFilter(Admin.message_all))
async def all_message(message: Message, bot: Bot, state: FSMContext) -> None:
    logging.info(f'Admin.message_id')
    message_all = message.html_text
    list_user = get_list_user()
    await message.answer(text='Рассылка запущена...')
    for user in list_user:
        result = get_telegram_user(user_id=user[1], bot_token=config.tg_bot.token)
        if 'result' in result:
            await asyncio.sleep(0.1)
            await bot.send_message(chat_id=user[1],
                                   text=message_all)
    await message.edit_text(text='Рассылка завершена...')
    await state.set_state(default_state)


@router.message()
async def all_message(message: Message, bot: Bot, state: FSMContext) -> None:
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
                await message.answer(text=f'Количество участников выполнивших {done_task} заданий: '
                                          f'{count_raffle_task}\n')
        if message.text == '/send_remember':
            logging.info(f'all_message-/send_remember')
            await send_new_raffle(bot=bot)

        if '/send_message' in message.text:
            logging.info(f'all_message-/send_message')
            send = message.text.split('_')
            if send[2] == "all":
                await message.answer(text='Пришлите текст чтобы его отправить всем пользователям бота')
                await state.set_state(Admin.message_all)
            else:
                try:
                    id_user = int(send[2])
                    info_user = get_info_user(id_user)
                    if info_user:
                        result = get_telegram_user(user_id=id_user, bot_token=config.tg_bot.token)
                        if 'result' in result:
                            await message.answer(text=f'Пришлите текст чтобы его отправить пользователю @{info_user[2]}')
                            await state.update_data(id_user=id_user)
                            await state.set_state(Admin.message_id)
                        else:
                            await message.answer(text=f'Бот не нашел пользователя {info_user[2]}.'
                                                      f' Возможно он его заблокировал')
                    else:
                        await message.answer(text=f'Бот не нашел пользователя {id_user} в БД')
                except:
                    await message.answer(text=f'Пришлите после команды /send_message_ id телеграм пользователя')
