import contextlib
import datetime
import sqlite3
import os

from constants import DB_SQLITE_FILENAME


@contextlib.contextmanager
def dbconn():
    try:
        conn = sqlite3.connect(DB_SQLITE_FILENAME)
        with conn:
            yield conn
    finally:
        conn.close()


def check_db_exists():
    return os.path.exists(DB_SQLITE_FILENAME)


def create_db():
    with dbconn() as conn:
        cur = conn.cursor()
        with open('create_hours_db.sql') as create_db_script:
            cur.execute(create_db_script.read())


def check_or_create_db():
    if check_db_exists():
        return
    create_db()


def insert_worktime(worktime):
    date = datetime.date.today()
    with dbconn() as conn:
        cursor = conn.cursor()
        query = 'insert into worktimes (workday, worktime) values (?, ?);'
        cursor.execute(query, (date, worktime))
    print('Worktime', worktime, 'added for', date)


def get_all_worktimes():
    with dbconn() as conn:
        cursor = conn.cursor()
        query = 'select id, workday, worktime from worktimes;'
        result = cursor.execute(query)
        return result.fetchall()


def check_id(id_):
    with dbconn() as conn:
        cursor = conn.cursor()
        query = 'select id from worktimes where id=?;'
        result = cursor.execute(query, (id_,))
        return any(result.fetchall())


def remove_worktime(id_):
    if check_id(id_):
        with dbconn() as conn:
            cursor = conn.cursor()
            query = 'delete from worktimes where id=?;'
            cursor.execute(query, (id_,))
    else:
        print('id', id_, 'does not exist')


def filter_by_month(month):
    month = str(month).zfill(2)
    with dbconn() as conn:
        cursor = conn.cursor()
        query = 'select id, workday, worktime from worktimes where strftime("%m", workday) = ?;'
        result = cursor.execute(query, (month,))
        return result.fetchall()
