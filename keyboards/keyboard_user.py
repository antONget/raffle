from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging


def keyboards_start_admin() -> ReplyKeyboardMarkup:
    logging.info("keyboards_user")
    button_1 = KeyboardButton(text='Задания')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1]],
        resize_keyboard=True
    )
    return keyboard


def keyboard_start_user() -> None:
    logging.info("keyboard_start_user")
    button_1 = InlineKeyboardButton(text='Соглашаюсь',
                                    callback_data='approval')
    button_2 = InlineKeyboardButton(text='Хочу узнать все условия',
                                    callback_data='condition')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2]],
    )
    return keyboard


def keyboard_condition() -> None:
    logging.info("keyboard_start_user")
    button_1 = InlineKeyboardButton(text='ГОТОВ(а)!',
                                    callback_data='approval')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1]],
    )
    return keyboard


def keyboard_get_username() -> None:
    logging.info("keyboard_start_user")
    button_1 = InlineKeyboardButton(text='Да',
                                    callback_data='confirm_username')
    button_2 = InlineKeyboardButton(text='Нет',
                                    callback_data='not_confirm_username')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2]],
    )
    return keyboard


def keyboards_get_contact() -> ReplyKeyboardMarkup:
    logging.info("keyboards_get_contact")
    button_1 = KeyboardButton(text='Отправить свой контакт ☎️', request_contact=True)
    button_2 = KeyboardButton(text='Отмена')
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_1], [button_2]],
        resize_keyboard=True
    )
    return keyboard


def keyboard_confirm_phone() -> None:
    logging.info("keyboard_confirm_phone")
    button_1 = InlineKeyboardButton(text='Верно',
                                    callback_data='confirm_username')
    button_2 = InlineKeyboardButton(text='Назад',
                                    callback_data='getphone_back')
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1], [button_2]],
    )
    return keyboard