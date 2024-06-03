import asyncio
import time

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, or_f

from config_data.config import Config, load_config
from module.data_base import get_message_content, create_table_list_raffle, add_user_list_raffle, get_info_user, set_done_task, get_list_last_raffle, get_list_user, get_info_user_raffle
from keyboards.keyboard_raffle import keyboard_task
import requests
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.context import FSMContext
import random
from aiogram.fsm.state import State, StatesGroup, default_state

router = Router()
user_dict = {}
config: Config = load_config()


class User(StatesGroup):
    username = State()
TEST_WEEK_DAY = 0
TEST_LIST_TIME = []
for i in range(7):
    minute = check_day = datetime.now().minute - 4 + i * 2
    TEST_LIST_TIME.append(minute)
# scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
# scheduler.start()
print(TEST_LIST_TIME)


def get_telegram_user(user_id, bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getChat'
    data = {'chat_id': user_id}
    response = requests.post(url, data=data)
    return response.json()


@router.callback_query(F.data == 'confirm_username')
async def task_monday(callback: CallbackQuery, state: FSMContext, bot: Bot, num_task: int = 0) -> None:
    logging.info(f'task_monday: {callback.message.chat.id}')
    # получаем день недели
    week_day = datetime.today().weekday()
    check_day = datetime.now().minute
    LIST_WEEKDAY = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    # await callback.message.answer(
    #     text=f'{LIST_WEEKDAY[num_task]}:{TEST_LIST_TIME[num_task + 2]}-{TEST_LIST_TIME[num_task + 3]}')
    # if TEST_LIST_TIME[2] <= check_day < TEST_LIST_TIME[3]:
    # если сегодня понедельник
    if week_day == 0:
        # создаем таблицу участников если еще не создана
        create_table_list_raffle()
        # дата розыгрыша в ближайшую субботу
        current_date = datetime.now() + timedelta(days=5)
        date_raffle = current_date.strftime('%d/%m/%Y')
        await state.update_data(date_raffle=date_raffle)
        # добавляем пользователя в базу данных
        add_user_list_raffle(date_raffle=date_raffle,
                             id_telegram=callback.message.chat.id,
                             count_task=0)
        # await get_task_monday(num_task=0, bot=bot)
        # получаем контент
        message_content = get_message_content(id_message=num_task+1)
        if '\\n' in message_content[2]:
            text = message_content[2].replace('\\n', '\n')
        else:
            text = message_content[2]
        if message_content[3] == 'none':
            await callback.message.answer(text=text,
                                          reply_markup=keyboard_task(num_task=num_task),
                                          parse_mode='html')
        else:
            await callback.message.answer_photo(photo=message_content[3],
                                                caption=text,
                                                reply_markup=keyboard_task(num_task=num_task),
                                                parse_mode='html')
        # количество выполненных задач
        user_dict[callback.message.chat.id] = await state.get_data()
        if 'done_task' not in user_dict[callback.message.chat.id].keys():
            await state.update_data(done_task=0)
        # # первое досыльное сообщение
        await asyncio.sleep(1 * 60 * 60)
        # await asyncio.sleep(1 * 10 * 1)
        user_dict[callback.message.chat.id] = await state.get_data()
        print(user_dict[callback.message.chat.id])
        list_task_name = ['первое', 'второе', 'третье', 'четвертое', 'пятое']
        # если количество выполненных заданий не изменилось и
        info_user_raffle = get_info_user_raffle(id_telegram=callback.message.chat.id, date_raffle=date_raffle)
        if info_user_raffle[3] == num_task and datetime.today().weekday() == 6:
        # if info_user_raffle[3] == num_task and (TEST_LIST_TIME[num_task+2] <= check_day < TEST_LIST_TIME[num_task+3]):#datetime.today().weekday() == TEST_WEEK_DAY:#check_day:
            await callback.message.answer(text=f'Выше мы прислали тебе {list_task_name[0]} задание!\n'
                                               f'Оно выполнено?\n\n'
                                               f'Если нет - скорее выполняй и не забудь сделать и сохранить скриншот,'
                                               f' а после нажать кнопку "Выполнено" ниже.',
                                          reply_markup=keyboard_task(num_task=num_task))
            await asyncio.sleep(3 * 60 * 60)
            # await asyncio.sleep(3 * 10 * 1)
            user_dict[callback.message.chat.id] = await state.get_data()
            info_user_raffle = get_info_user_raffle(id_telegram=callback.message.chat.id, date_raffle=date_raffle)
            # if info_user_raffle[3] == num_task and datetime.today().weekday() == 6:
            if info_user_raffle[3] == num_task and (TEST_LIST_TIME[num_task+2] <= check_day < TEST_LIST_TIME[num_task+3]):#datetime.today().weekday() == TEST_WEEK_DAY:#check_day:
                await callback.message.answer(text=f'Осталось совсем немного времени, чтобы выполнить {list_task_name[0]} задание.'
                                                   f' Больше напоминать не будем!\n\n'
                                                   f'Скорее выполняй! Не забудь сделать и сохранить скриншот, а после'
                                                   f' нажать кнопку "Выполнено" ниже.',
                                              reply_markup=keyboard_task(num_task=num_task))

    else:
        await callback.message.answer(text='Отлично! Теперь дождись понедельника и приступай к заданиям.')
        create_table_list_raffle()
        # дата розыгрыша
        week_day = datetime.today().weekday()
        list_plus_date_raffle = [5, 4, 3, 2, 1, 7, 6]
        current_date = datetime.now() + timedelta(days=list_plus_date_raffle[week_day])
        date_raffle = current_date.strftime('%d/%m/%Y')
        await state.update_data(date_raffle=date_raffle)
        # информация о пользователе
        add_user_list_raffle(date_raffle=date_raffle,
                             id_telegram=callback.message.chat.id,
                             count_task=0)


@router.callback_query(F.data == 'decline_task')
async def confirm_decline_task(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'confirm_decline_task: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    date_raffle = user_dict[callback.message.chat.id]['date_raffle']
    set_done_task(id_telegram=callback.message.chat.id, date_raffle=date_raffle, done_task=-1)
    await state.update_data(done_task=-1)
    # scheduler.remove_all_jobs()
    await callback.message.answer(text=f'Не знаем почему ты решил(а) отказаться от участия, но уважаем твоë решение.'
                                       f' Если вдруг передумаешь, нажми /start')


@router.callback_query(F.data.startswith('done_task'))
async def confirm_done_task(callback: CallbackQuery, state: FSMContext) -> None:
    logging.info(f'confirm_done_task: {callback.message.chat.id}')
    user_dict[callback.message.chat.id] = await state.get_data()
    check_day = datetime.now().minute
    num_task = int(callback.data.split('_')[2])
    if num_task < 4:
        # if TEST_LIST_TIME[num_task + 2] <= check_day < TEST_LIST_TIME[num_task + 3]:
        if num_task == datetime.today().weekday():
            text_done_task = ['Первое задание ✅\n\nЖди завтра второе!',
                              'Так держать! Уже два задания из пяти сделано✅',
                              '✅Ты так легко выполнил и третье задание!\n\nЗавтра отправлю тебе еще одно.',
                              '✅ Круто! Ты понимаешь, что ты в шаге от того, чтобы выполнить все 5 наших заданий и стать участником розыгрыша?!\n\nОсталось только одно задание. Жди его завтра!',
                              '✅ Огонь! Ты выполнил все задания!\n\nИ теперь участвуешь в розыгрыше главного приза, который пройдёт в субботу!']
            await callback.message.answer(text=text_done_task[num_task])
            # if num_task == 4:
            #     await callback.message.answer(text='Мы благодарим тебя за активное участие в нашем конкурсе!\n\n'
            #                                        'Надеемся, у тебя получилось поближе познакомиться с нами и было приятно выполнять наши несложные задания.\n\n'
            #                                        'Результаты будут объявлены завтра в 10:00!')
            date_raffle = user_dict[callback.message.chat.id]['date_raffle']
            set_done_task(id_telegram=callback.message.chat.id, date_raffle=date_raffle, done_task=num_task+1)
        else:
            list_task_name = ['первое', 'второе', 'третье', 'четвертое', 'пятое']
            await callback.message.answer(text=f'Сожалеем, но ты не успел выполнить {list_task_name[num_task]} задание во время! И не можешь продолжить борьбу за главный приз.\n\n'
                                               f'Но мы напомним тебе о новом розыгрыше в понедельник.')
    else:
        # if TEST_LIST_TIME[num_task + 2] <= check_day:
        if num_task == datetime.today().weekday():
            text_done_task = ['Первое задание ✅\n\nЖди завтра второе!',
                              'Так держать! Уже два задания из пяти сделано✅',
                              '✅Ты так легко выполнил и третье задание!\n\nЗавтра отправлю тебе еще одно.',
                              '✅ Круто! Ты понимаешь, что ты в шаге от того, чтобы выполнить все 5 наших заданий и стать участником розыгрыша?!\n\nОсталось только одно задание. Жди его завтра!',
                              '✅ Огонь! Ты выполнил все задания!\n\nИ теперь участвуешь в розыгрыше главного приза, который пройдёт в субботу!']
            await callback.message.answer(text=text_done_task[num_task])
            if num_task == 4:
                await callback.message.answer(text='Мы благодарим тебя за активное участие в нашем конкурсе!\n\n'
                                                   'Надеемся, у тебя получилось поближе познакомиться с нами и было приятно выполнять наши несложные задания.\n\n'
                                                   'Результаты будут объявлены завтра в 10:00!')
            date_raffle = user_dict[callback.message.chat.id]['date_raffle']
            set_done_task(id_telegram=callback.message.chat.id, date_raffle=date_raffle, done_task=num_task + 1)
        else:
            list_task_name = ['первое', 'второе', 'третье', 'четвертое', 'пятое']
            await callback.message.answer(text=f'Сожалеем, но ты не успел выполнить {list_task_name[num_task]} задание во время! И не можешь продолжить борьбу за главный приз.\n\n'
                                               f'Но мы напомним тебе о новом розыгрыше в понедельник.')

async def get_task_monday(num_task: int, bot: Bot):
    list_raffle = get_list_last_raffle(done_task=num_task)
    # получаем контент
    message_content = get_message_content(id_message=num_task + 1)
    print(message_content)
    text = message_content[2]
    if '\\n' in message_content[2]:
        text = message_content[2].replace('\\n', '\n')
    print(message_content)
    if message_content[3] == 'none':
        for user_raffle in list_raffle:
            if user_raffle[3] != -1 or user_raffle[3] == num_task:
                result = get_telegram_user(user_id=user_raffle[2], bot_token=config.tg_bot.token)
                if 'result' in result:
                    await bot.send_message(chat_id=user_raffle[2],
                                           text=text,
                                           reply_markup=keyboard_task(num_task=num_task),
                                           parse_mode='html')
    else:
        for user_raffle in list_raffle:
            print(user_raffle)
            if user_raffle[3] != -1 or user_raffle[3] == num_task:
                result = get_telegram_user(user_id=user_raffle[2], bot_token=config.tg_bot.token)
                if 'result' in result:
                    await bot.send_photo(chat_id=user_raffle[2],
                                         photo=message_content[3],
                                         caption=text,
                                         reply_markup=keyboard_task(num_task=num_task),
                                         parse_mode='html')

    # первое досыльное сообщение
    await asyncio.sleep(1 * 60 * 60)
    # await asyncio.sleep(1 * 10 * 1)
    list_task_name = ['первое', 'второе', 'третье', 'четвертое', 'пятое']
    # если количество выполненных заданий не изменилось и
    check_day = datetime.now().minute
    list_raffle = get_list_last_raffle(done_task=num_task)
    # print('214', num_task, list_raffle)
    for user_raffle in list_raffle:
        # if (user_raffle[3] != -1 or user_raffle[3] == num_task) and (TEST_LIST_TIME[num_task + 2] <= check_day < TEST_LIST_TIME[num_task + 3]):  # datetime.today().weekday() == TEST_WEEK_DAY:#check_day:
        if (user_raffle[3] != -1 or user_raffle[3] == num_task) and datetime.today().weekday() == 0:
            result = get_telegram_user(user_id=user_raffle[2], bot_token=config.tg_bot.token)
            if 'result' in result:
                await bot.send_message(chat_id=user_raffle[2],
                                       text=f'Выше мы прислали тебе {list_task_name[user_raffle[3]]} задание!\n'
                                            f'Оно выполнено?\n\n'
                                            f'Если нет - скорее выполняй и не забудь сделать и сохранить скриншот,'
                                            f' а после нажать кнопку "Выполнено" ниже.',
                                       reply_markup=keyboard_task(num_task=num_task))
            await asyncio.sleep(3 * 60 * 60)
            # await asyncio.sleep(1 * 30 * 1)
            list_raffle = get_list_last_raffle(done_task=num_task)
            for user_raffle in list_raffle:
                if (user_raffle[3] != -1 or user_raffle[3] == num_task) and datetime.today().weekday() == 0:
                # if (user_raffle[3] != -1 or user_raffle[3] == num_task) and (TEST_LIST_TIME[num_task + 2] <= check_day < TEST_LIST_TIME[num_task + 3]):
                    result = get_telegram_user(user_id=user_raffle[2], bot_token=config.tg_bot.token)
                    if 'result' in result:
                        await bot.send_message(chat_id=user_raffle[2],
                                               text=f'Осталось совсем немного времени, чтобы выполнить {list_task_name[user_raffle[3]]} задание.'
                                                    f' Больше напоминать не будем!\n\n'
                                                    f'Скорее выполняй! Не забудь сделать и сохранить скриншот, а после'
                                                    f' нажать кнопку "Выполнено" ниже.',
                                               reply_markup=keyboard_task(num_task=num_task))


async def select_winer(bot: Bot):
    list_raffle = get_list_last_raffle(done_task=5)
    if len(list_raffle) >= 5:
        list_winer = random.choice(list_raffle, 5)
    else:
        list_winer = list_raffle
    text = ''
    for winer in list_winer:
        infor_user = get_info_user(telegram_id=winer[2])
        text += f'{infor_user[2]}\n'
        result = get_telegram_user(user_id=winer[2], bot_token=config.tg_bot.token)
        if 'result' in result:
            await bot.send_message(chat_id=winer[2],
                                   text='Вы стати победителем этой недели. Поздравляем! Для получения выигрыша, напишите менеджеру')
    list_user = get_list_user()
    for user in list_user:
        result = get_telegram_user(user_id=user[1], bot_token=config.tg_bot.token)
        if 'result' in result:
            await bot.send_message(chat_id=user[1],
                                   text=f'Список победителей этой недели:\n'
                                        f'{text}')
