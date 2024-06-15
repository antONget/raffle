from aiogram.types import Message

import sqlite3
from config_data.config import Config, load_config
import logging
from datetime import datetime, timedelta

config: Config = load_config()
db = sqlite3.connect('database.db', check_same_thread=False, isolation_level='EXCLUSIVE')


# СОЗДАНИЕ ТАБЛИЦ - users
def create_table_users() -> None:
    """
    Создание таблицы верифицированных пользователей
    :return: None
    """
    logging.info("table_users")
    with db:
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            telegram_id INTEGER,
            username TEXT
        )""")
        db.commit()


# # MAIN - добавление супер-админа в таблицу users
# def add_admin(id_admin: int, user_name: str) -> None:
#     """
#     Добавление супер-админа в таблицу пользователей
#     :param id_admin: id_telegram супер-админа
#     :param user_name: имя супер-админа в телеграм
#     :return:
#     """
#     logging.info(f'add_super_admin')
#     with db:
#         sql = db.cursor()
#         sql.execute('SELECT telegram_id FROM users')
#         list_user = [row[0] for row in sql.fetchall()]
#
#         if int(id_admin) not in list_user:
#             sql.execute(f'INSERT INTO users (telegram_id, username, is_admin, list_category, rating) '
#                         f'VALUES ({id_admin}, "{user_name}", 1, "0", 0)')
#             db.commit()


def add_user(id_user: int, user_name: str) -> None:
    """
    Добавление супер-админа в таблицу пользователей
    :param id_user: id_telegram пользователя
    :param user_name: имя пользователя в телеграм
    :return:
    """
    logging.info(f'add_super_admin')
    with db:
        sql = db.cursor()
        sql.execute('SELECT telegram_id FROM users')
        list_user = [row[0] for row in sql.fetchall()]

        if int(id_user) not in list_user:
            sql.execute(f'INSERT INTO users (telegram_id, username) '
                        f'VALUES ({id_user}, "{user_name}")')
            db.commit()


def set_username(username: str, telegram_id: int):
    """
    Разжаловать пользователя с id_telegram из администраторов
    :param username:
    :param telegram_id:
    :return:
    """
    logging.info(f'set_username')
    with db:
        sql = db.cursor()
        sql.execute('UPDATE users SET username = ? WHERE telegram_id = ?', (username, telegram_id))
        db.commit()


def get_list_user() -> list:
    """
    Получить список верифицированных пользователей
    :return:
    """
    logging.info(f'get_list_user')
    with db:
        sql = db.cursor()
        sql.execute('SELECT * FROM users')
        list_users = [row for row in sql.fetchall()]
        return list_users


# # АДМИНИСТРАТОРЫ - Назначить пользователя администратором
# def set_admins(telegram_id: int):
#     """
#     Назначение пользователя с id_telegram администратором
#     :param telegram_id:
#     :return:
#     """
#     logging.info(f'set_admins')
#     with db:
#         sql = db.cursor()
#         sql.execute('UPDATE users SET is_admin = ? WHERE telegram_id = ?', (1, telegram_id))
#         db.commit()


# # АДМИНИСТРАТОРЫ - Разжаловать пользователя из администраторов
# def set_notadmins(telegram_id):
#     """
#     Разжаловать пользователя с id_telegram из администраторов
#     :param telegram_id:
#     :return:
#     """
#     logging.info(f'set_notadmins')
#     with db:
#         sql = db.cursor()
#         sql.execute('UPDATE users SET is_admin = ? WHERE telegram_id = ?', (0, telegram_id))
#         db.commit()


# # ПАРТНЕР - Получить список пользователей не являющихся администратором
# def get_list_notadmins_mailer() -> list:
#     """
#     Получить список верифицированных пользователей не являющихся администратором
#     :return:
#     """
#     logging.info(f'get_list_notadmins')
#     with db:
#         sql = db.cursor()
#         sql.execute('SELECT * FROM users WHERE is_admin = ?', (0,))
#         list_notadmins = [row for row in sql.fetchall()]
#         return list_notadmins


# # ПАРТНЕР - получение списка администраторов
# def get_list_admins() -> list:
#     """
#     Получение списка администраторов
#     :return:
#     """
#     logging.info(f'get_list_admins')
#     with db:
#         sql = db.cursor()
#         sql.execute('SELECT telegram_id, username FROM users WHERE is_admin = ?', (1,))
#         list_admins = [row for row in sql.fetchall()]
#         return list_admins


# # # ПОЛЬЗОВАТЕЛЬ - имя пользователя по его id
# def get_user(telegram_id: int):
#     """
#     ПОЛЬЗОВАТЕЛЬ - имя пользователя по его id
#     :param telegram_id:
#     :return:
#     """
#     logging.info(f'get_user')
#     with db:
#         sql = db.cursor()
#         return sql.execute('SELECT username FROM users WHERE telegram_id = ?', (telegram_id,)).fetchone()


# # ПОЛЬЗОВАТЕЛЬ - данные пользователя по его id телеграмм
def get_info_user(telegram_id: int):
    """
    ПОЛЬЗОВАТЕЛЬ - имя пользователя по его id
    :param telegram_id:
    :return:
    """
    logging.info(f'get_user')
    with db:
        sql = db.cursor()
        return sql.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,)).fetchone()


# # ПОЛЬЗОВАТЕЛЬ - получить список категорий
# def get_select(telegram_id: int):
#     """
#     Получаем флаг пользователя в команде
#     :param telegram_id:
#     :return:
#     """
#     logging.info(f'set_select')
#     with db:
#         sql = db.cursor()
#         in_command = sql.execute('SELECT list_category FROM users WHERE telegram_id = ?', (telegram_id,)).fetchone()
#         return in_command[0]


# # ПОЛЬЗОВАТЕЛЬ - обновляем список категорий
# def set_select(list_category: str, telegram_id: int):
#     """
#     Обновление списка категорий
#     :param list_category: список категорий
#     :param telegram_id:
#     :return:
#     """
#     logging.info(f'set_select')
#     with db:
#         sql = db.cursor()
#         sql.execute('UPDATE users SET list_category = ? WHERE telegram_id = ?', (list_category, telegram_id))
#         db.commit()

#
# # СОЗДАНИЕ ТАБЛИЦ - order
# def create_table_order() -> None:
#     """
#     Создание таблицы проведенных игр
#     :return: None
#     """
#     logging.info("create_table_order")
#     with db:
#         sql = db.cursor()
#         sql.execute("""CREATE TABLE IF NOT EXISTS orders(
#             id INTEGER PRIMARY KEY,
#             time_order TEXT,
#             description_order TEXT,
#             contact_order TEXT,
#             category INTEGER,
#             mailer_order TEXT,
#             status TEXT,
#             id_user INTEGER,
#             amount INTEGER,
#             report TEXT
#         )""")
#         db.commit()
#
#
# # ЗАЯВКА - добавление заявки
# def add_order(time_order: str, description_order: str, contact_order: str, category: str, mailer_order: str, status: str, id_user: int, amount: int, report: str) -> None:
#     """
#     Добавление заявки в базу
#     :param time_order:
#     :param description_order:
#     :param contact_order:
#     :param category:
#     :param mailer_order:
#     :param status:
#     :param id_user:
#     :param amount:
#     :return:
#     """
#     logging.info(f'add_category')
#     with db:
#         sql = db.cursor()
#         sql.execute(f'INSERT INTO orders (time_order, description_order, contact_order, category, mailer_order, status, id_user, amount, report)'
#                     f' VALUES ("{time_order}", "{description_order}", "{contact_order}", {category}, "{mailer_order}", "{status}", {id_user}, {amount}, "{report}")')
#         db.commit()
#
#
# # ЗАЯВКА - получение списка заявок
# def get_list_order() -> list:
#     """
#     ЗАЯВКА - получение списка заявок
#     :return: list(order:str)
#     """
#     logging.info(f'get_list_order')
#     with db:
#         sql = db.cursor()
#         sql.execute('SELECT * FROM orders ORDER BY id')
#         list_category = [row for row in sql.fetchall()]
#         return list_category
#
#
# # ЗАЯВКА - получение списка заявок исполнителя
# def get_list_order_id(id_user: int) -> list:
#     """
#     ЗАЯВКА - получение списка заявок исполнителя
#     :return: list(order:str)
#     """
#     logging.info(f'get_list_order')
#     with db:
#         sql = db.cursor()
#         sql.execute('SELECT * FROM orders WHERE id_user = ? ORDER BY id', (id_user,))
#         list_category = [row for row in sql.fetchall()]
#         return list_category
#
#
# # ЗАЯВКА - получение заявки по id
# def get_order_id(id_order: int):
#     """
#     ЗАЯВКА - получение заявки по id
#     :param id_order:
#     :return:
#     """
#     logging.info(f'get_order_id')
#     with db:
#         sql = db.cursor()
#         sql.execute('SELECT * FROM orders WHERE id =?', (id_order,))
#         return sql.fetchone()
#
#
# # ЗАЯВКА - обновляем список рассылки
# def set_mailer_order(id_order: int, mailer_order: str):
#     """
#     Обновляем список рассылки для заказа
#     :param id_order:
#     :param mailer_order:
#     :return:
#     """
#     logging.info(f'set_select')
#     with db:
#         sql = db.cursor()
#         sql.execute('UPDATE orders SET mailer_order = ? WHERE id = ?', (mailer_order, id_order,))
#         db.commit()
#
#
# # ЗАЯВКА - обновляем статус заявки
# def set_status_order(id_order: int, status: str):
#     """
#     Обновляем список рассылки для заказа
#     :param id_order:
#     :param status:
#     :return:
#     """
#     logging.info(f'set_select')
#     with db:
#         sql = db.cursor()
#         sql.execute('UPDATE orders SET status = ? WHERE id = ?', (status, id_order,))
#         db.commit()
#
#
# # ЗАЯВКА - обновляем исполнителя заявки
# def set_user_order(id_order: int, id_user: int):
#     """
#     Обновляем исполнителя заказа
#     :param id_order:
#     :param id_user:
#     :return:
#     """
#     logging.info(f'set_select')
#     with db:
#         sql = db.cursor()
#         sql.execute('UPDATE orders SET id_user = ? WHERE id = ?', (id_user, id_order,))
#         db.commit()
#
#
# # ЗАЯВКА - обновляем статус заявки
# def set_report_order(id_order: int, report: str):
#     """
#     Обновляем исполнителя заказа
#     :param id_order:
#     :param report:
#     :return:
#     """
#     logging.info(f'set_select')
#     with db:
#         sql = db.cursor()
#         sql.execute('UPDATE orders SET report = ? WHERE id = ?', (report, id_order,))
#         db.commit()
#
#
# # ЗАЯВКА - обновляем сумму заявки
# def set_amount_order(id_order: int, amount: int):
#     """
#     Обновляем исполнителя заказа
#     :param id_order:
#     :param amount:
#     :return:
#     """
#     logging.info(f'set_select')
#     with db:
#         sql = db.cursor()
#         sql.execute('UPDATE orders SET amount = ? WHERE id = ?', (amount, id_order,))
#         db.commit()
#
#
# # СОЗДАНИЕ ТАБЛИЦ - category
# def create_table_category() -> None:
#     """
#     Создание таблицы проведенных игр
#     :return: None
#     """
#     logging.info("create_table_category")
#     with db:
#         sql = db.cursor()
#         sql.execute("""CREATE TABLE IF NOT EXISTS category(
#             id INTEGER PRIMARY KEY,
#             name_category TEXT
#         )""")
#         db.commit()
#
#
# # КАТЕГОРИЯ - добавление категории в базу
# def add_category(category: str) -> None:
#     """
#     Добавление токена в таблицу пользователей с указанием кто его добавил
#     :param category:
#     :return:
#     """
#     logging.info(f'add_category')
#     with db:
#         sql = db.cursor()
#         sql.execute(f'INSERT INTO category (name_category) VALUES ("{category}")')
#         db.commit()
#
#
# # КАТЕГОРИЯ - получение списка категорий
# def get_list_category() -> list:
#     """
#     КАТЕГОРИЯ - получение списка категорий
#     :return: list(category:str)
#     """
#     logging.info(f'get_list_category')
#     with db:
#         sql = db.cursor()
#         sql.execute('SELECT * FROM category ORDER BY id')
#         list_category = [row for row in sql.fetchall()]
#         return list_category
#
#
# # КАТЕГОРИЯ - удаление категории по его id
# def delete_category(category_id: int):
#     """
#     КАТЕГОРИЯ - удаление категории по его id
#     :param category_id:
#     :return:
#     """
#     logging.info(f'delete_category')
#     with db:
#         sql = db.cursor()
#         sql.execute('DELETE FROM category WHERE id = ?', (category_id,))
#         db.commit()


# КАТЕГОРИЯ - получение названия категории ее id
def get_title_category(id_category: int) -> list:
    """
    КАТЕГОРИЯ - получение списка категорий
    :return: list(category:str)
    """
    logging.info(f'get_list_category: {id_category}')
    with db:
        sql = db.cursor()
        sql.execute('SELECT * FROM category WHERE id = ?', (id_category,))
        return sql.fetchone()[1]


def create_table_message_content() -> None:
    """
    Создание таблицы верифицированных пользователей
    :return: None
    """
    logging.info("create_table_message_content")
    with db:
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS message_content(
            id INTEGER PRIMARY KEY,
            title_text TEXT,
            message_text TEXT,
            message_image TEXT DEFAULT 'none'
        )""")
        db.commit()


def get_message_content(id_message: int) -> str:
    logging.info(f'get_message_text: {id_message}')
    with db:
        sql = db.cursor()
        sql.execute('SELECT * FROM message_content WHERE id = ?', (id_message,))
        return sql.fetchone()


def add_message_text(message_text: str) -> None:
    logging.info(f'add_message_text')
    with db:
        sql = db.cursor()
        sql.execute(f'INSERT INTO message_content (message_text) VALUES ("{message_text}")')
        db.commit()


def set_message_text(id_message: int, message_text: str):
    logging.info(f'set_message_text')
    with db:
        sql = db.cursor()
        sql.execute('UPDATE message_content SET message_text = ? WHERE id = ?', (message_text, id_message,))
        db.commit()


def set_message_image(id_message: int, message_image: str):
    logging.info(f'set_message_text')
    with db:
        sql = db.cursor()
        sql.execute('UPDATE message_content SET message_image = ? WHERE id = ?', (message_image, id_message,))
        db.commit()


def create_table_list_raffle() -> None:
    logging.info("create_table_message_content")
    with db:
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS list_raffle(
            id INTEGER PRIMARY KEY,
            date_raffle TEXT,
            id_telegram INTEGER,
            count_task INTEGER DEFAULT 0
        )""")
        db.commit()


def add_user_list_raffle(date_raffle: str, id_telegram: int, count_task: int) -> None:
    logging.info(f'add_message_text')
    with db:
        sql = db.cursor()
        sql.execute('SELECT id_telegram FROM list_raffle WHERE date_raffle= ?', (date_raffle,))
        list_user = [row[0] for row in sql.fetchall()]
        if int(id_telegram) not in list_user:
            sql.execute(f'INSERT INTO list_raffle (date_raffle, id_telegram, count_task) VALUES ("{date_raffle}", {id_telegram}, {count_task})')
            db.commit()


def set_done_task(id_telegram: int, date_raffle: str, done_task: int):
    logging.info(f'set_done_task')
    with db:
        sql = db.cursor()
        sql.execute('UPDATE list_raffle SET count_task = ? WHERE id_telegram = ? AND date_raffle = ?', (done_task, id_telegram, date_raffle,))
        db.commit()

def get_last_date_raffle():
    logging.info(f'get_last_date_raffle')
    week_day = datetime.today().weekday()
    list_plus_date_raffle = [5, 4, 3, 2, 1, 0, 6]
    date_raffle = (datetime.now() + timedelta(days=list_plus_date_raffle[week_day])).strftime('%d/%m/%Y')
    return date_raffle
    # with db:
    #     sql = db.cursor()
    #     sql.execute('SELECT * FROM list_raffle')
    #     date_raffle = sql.fetchall()
    #     if len(date_raffle):
    #         return '15/06/2024'
    #         # return date_raffle[-1][1]
    #     else:
    #         return 0

def get_list_last_raffle(done_task: int) -> list:
    logging.info(f'get_list_rafle')
    date_raffle = get_last_date_raffle()
    if date_raffle:
        with db:
            sql = db.cursor()
            sql.execute('SELECT * FROM list_raffle WHERE count_task = ? AND date_raffle = ?', (done_task, date_raffle,))
            list_last_raffle = sql.fetchall()
            print(date_raffle)
            return list_last_raffle
    else:
        return 0


def get_list_last_raffle_all() -> list:
    logging.info(f'get_list_rafle')
    date_raffle = get_last_date_raffle()
    if date_raffle:
        with db:
            sql = db.cursor()
            sql.execute('SELECT * FROM list_raffle WHERE date_raffle = ?', (date_raffle,))
            list_last_raffle = sql.fetchall()
            print(date_raffle)
            return list_last_raffle
    else:
        return 0

def get_info_user_raffle(id_telegram: int, date_raffle: str) -> list:
    logging.info(f'get_list_rafle')
    with db:
        sql = db.cursor()
        sql.execute('SELECT * FROM list_raffle WHERE id_telegram = ? AND date_raffle = ?', (id_telegram, date_raffle,))
        date_raffle = sql.fetchone()
        print(date_raffle)
        return date_raffle