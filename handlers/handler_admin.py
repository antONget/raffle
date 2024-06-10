from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from filter.admin_filter import check_super_admin
from module.data_base import create_table_message_content, set_message_text, set_message_image
from keyboards.keyboard_admin import keyboard_super_admin, keyboard_cancel_change_task

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup, default_state

import logging

router = Router()
user_dict = {}

class Task(StatesGroup):
    post_task = State()


@router.message(F.text == 'Задания', lambda message: check_super_admin(message.chat.id))
async def process_change_task(message: Message) -> None:
    logging.info("process_change_task")
    """
    Запуск режима администратора супер-администратором
    :param message: 
    :return: 
    """
    create_table_message_content()
    await message.answer(text=f"Выберите задание для его изменения",
                         reply_markup=keyboard_super_admin())


@router.callback_query(F.data.startswith('task'))
async def select_change_task(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'select_change_task: {callback.message.chat.id}')
    number_task = callback.data.split('_')[1]
    await state.update_data(number_task=int(number_task))
    await callback.message.answer(text=f'Пришлите пост для {number_task} задания',
                                  reply_markup=keyboard_cancel_change_task())
    await state.set_state(Task.post_task)


@router.message(StateFilter(Task.post_task))
async def get_change_task(message: Message, state: FSMContext) -> None:
    logging.info("get_change_task")
    user_dict[message.chat.id] = await state.get_data()
    number_task = user_dict[message.chat.id]['number_task']
    if message.photo:
        logging.info(f'all_message message.photo')
        print(message.photo[-1].file_id)
        set_message_image(id_message=number_task, message_image=message.photo[-1].file_id)
        print(message)
        print(message.html_text)
        set_message_text(id_message=number_task, message_text=message.html_text)
        await message.answer(text='Задание обновлено')
    if message.text:
        print(message.html_text)
        set_message_text(id_message=number_task, message_text=message.html_text)
        set_message_image(id_message=number_task, message_image='none')
        await message.answer(text='Задание обновлено')
    await state.set_state(default_state)


@router.callback_query(F.data.startswith('cancel_change_task'))
async def select_change_task(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'select_change_task: {callback.message.chat.id}')
    await callback.message.answer(text='Действие отменено')
    await callback.answer()
