from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import logging


def keyboard_super_admin() -> None:
    logging.info("keyboard_super_admin")
    button_1 = InlineKeyboardButton(text='Задание 1',
                                    callback_data='task_1')
    button_2 = InlineKeyboardButton(text='Задание 2',
                                    callback_data='task_2')
    button_3 = InlineKeyboardButton(text='Задание 3',
                                    callback_data='task_3')
    button_4 = InlineKeyboardButton(text='Задание 4',
                                    callback_data='task_4')
    button_5 = InlineKeyboardButton(text='Задание 5',
                                    callback_data='task_5')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2], [button_3], [button_4], [button_5]],
    )
    return keyboard


def keyboard_cancel_change_task() -> None:
    logging.info("keyboard_super_admin")
    button_1 = InlineKeyboardButton(text='Отмена',
                                    callback_data='cancel_change_task')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1]],
    )
    return keyboard