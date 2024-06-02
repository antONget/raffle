from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, or_f

from config_data.config import Config, load_config
from module.data_base import create_table_users, add_user, set_username
from keyboards.keyboard_user import keyboards_start_admin, keyboard_start_user, keyboard_condition, \
    keyboard_get_username, keyboards_get_contact, keyboard_confirm_phone
from filter.admin_filter import check_super_admin

import logging
import re

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state

router = Router()
user_dict = {}
config: Config = load_config()


class User(StatesGroup):
    username = State()

def validate_russian_phone_number(phone_number):
    # Паттерн для российских номеров телефона
    # Российские номера могут начинаться с +7, 8, или без кода страны
    pattern = re.compile(r'^(\+7|8|7)?(\d{10})$')

    # Проверка соответствия паттерну
    match = pattern.match(phone_number)

    return bool(match)


@router.message(CommandStart())
async def process_start_command_user(message: Message) -> None:
    logging.info("process_start_command_user")
    """
    Запуск бота исполнителем
    :param message: 
    :return: 
    """
    create_table_users()

    add_user(id_user=message.chat.id, user_name=message.from_user.username)
    if check_super_admin(telegram_id=message.chat.id):
        await message.answer(text=f'Вы супер-администратор проекта и вам доступен режим правки заданий',
                             reply_markup=keyboards_start_admin())
    await message.answer(text=f'Приветствую, {message.from_user.first_name}!\n'
                              f'Если ты запустил(а) этого бота, значит хочешь стать одним из победителей еженедельного'
                              f' розыгрыша ХХХ рублей от НАС.\n\n'
                              f'От этого тебя отделяет всего 5 заданий. По одному в день!\n\n'
                              f'Соглашаешься на участие?',
                         reply_markup=keyboard_start_user())


@router.callback_query(F.data == 'condition')
async def read_condition(callback: CallbackQuery) -> None:
    logging.info(f'read_condition: {callback.message.chat.id}')
    await callback.message.answer(text=f'Слушай, условия простые, как раз-два-три!\\n'
                                       f'1. Каждый понедельник в этом боте тебе будет приходить приглашение участвовать в активностях новой недели. НЕ пропусти его, иначе не сможешь получать задания.\\n'
                                       f'2. C Пн по Пт будут приходит задания. Выполняй и не забудь нажать "Выполнено!".\n'
                                       f'Мы заботливо ДВАЖДЫ напомним тебе о необходимости выполнить новое задание.\n'
                                       f'Твоя задача успеть выполнить его до выхода следующего!\n\n'
                                       f'Увы, если хотя бы одно задание пропущено - не видать тебе приза. Но ты сможешь принять участие на следующей недели!\n\n'
                                       f'3. По субботам бот сам выбирает победителей среди тех, кто выполнит все задания и присылает список из 10 имен.\n\n'
                                       f'Для получения денежного приза победители должны будут предоставить скрины и др. подтверждения выполнения всех 5 заданий!\n\n'
                                       f'Ну что, готов?',
                                  reply_markup=keyboard_condition())


@router.callback_query(F.data == 'approval')
async def select_approval(callback: CallbackQuery) -> None:
    logging.info(f'select_approval: {callback.message.chat.id}')
    await callback.message.answer(text=f'Отлично! Теперь тебя нужно внести в базу участников!\n'
                                       f'Записать, как @{callback.from_user.username}*?\n\n'
                                       f'* - если твой ник не отобразился, нажми «Нет».',
                                  reply_markup=keyboard_get_username())


@router.callback_query(F.data == 'not_confirm_username')
async def select_not_confirm_username(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'select_not_confirm_username: {callback.message.chat.id}')
    await callback.message.answer(text='Тогда ты можешь указать ссылку на свой Телеграм или контактный номер для связи:',
                                  reply_markup=keyboards_get_contact())
    await state.set_state(User.username)


@router.message(F.text == 'Отмена', StateFilter(User.username))
async def process_start_command_user(message: Message, state: FSMContext) -> None:
    logging.info("process_start_command_user")
    await state.set_state(default_state)
    await process_start_command_user(message=message, state=state)


@router.message(or_f(F.text, F.contact), StateFilter(User.username))
async def process_start_command_user(message: Message, state: FSMContext) -> None:
    logging.info("process_start_command_user")
    if message.contact:
        phone = str(message.contact.phone_number)
    else:
        phone = message.text
        if not validate_russian_phone_number(phone):
            await message.answer(text="Неверный формат номера. Повторите ввод, например 89991112222:")
            return
    await state.update_data(username=phone)
    set_username(username=str(phone), telegram_id=message.chat.id)
    await state.set_state(default_state)
    await message.answer(text=f'Записываю, {phone}. Верно?',
                         reply_markup=keyboard_confirm_phone())


@router.callback_query(F.data == 'getphone_back')
async def confirm_get_phone(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'confirm_get_phone: {callback.message.chat.id}')
    await select_not_confirm_username(callback=callback, state=state)
