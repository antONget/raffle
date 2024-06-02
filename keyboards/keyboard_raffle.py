from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import logging


def keyboard_task(num_task: int) -> None:
    logging.info("keyboard_confirm_phone")
    button_1 = InlineKeyboardButton(text='Выполнено',
                                    callback_data=f'done_task_{num_task}')
    button_2 = InlineKeyboardButton(text='Отказаться от участия',
                                    callback_data='decline_task')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2]],
    )
    return keyboard