import sqlite3
import sys
import traceback
from sqlite3 import Error



def sql_connection():
    try:
        con = sqlite3.connect("../twitdb.db")
        print("Нормес прошло. ДБ создано")
        return con
    except Error:
        print(Error)


def sql_table(con):
    cursObj = con.cursor()
    try:
        cursObj.execute('CREATE TABLE IF NOT EXISTS twits (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, tweet text NOT NULL, chatid INTEGER NOT NULL)')
        print("Table created")
        con.commit()
    except Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


def create_twitter_table(con):
    cursObj = con.cursor()
    try:
        cursObj.execute('CREATE TABLE IF NOT EXISTS twitterkey (chatid INTEGER PRIMARY KEY NOT NULL, key text NOT NULL, secret text NOT NULL)')
        print("Table twitterkey created")
        con.commit()
    except Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


def sql_insert_twitter(con, entetys):
    cursorObj = con.cursor()
    try:
        cursorObj.execute("INSERT INTO twitterkey (chatid, key, secret) VALUES (?,?,?)", entetys)
        print("Done")
        con.commit()
    except Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


def sql_insert(con, entetys):
    cursorObj = con.cursor()
    try:
        cursorObj.execute("INSERT INTO twits (tweet, chatid) VALUES (?,?)", entetys)
        print("Done")
        con.commit()
    except Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


def sql_getRow(con):
    cursorObj = con.cursor()
    try:
        cursorObj.execute("SELECT * FROM twits")
        raws = cursorObj.fetchall()
        k = len(raws)
        print(k)
        return k
    except Error:
        print(Error)


def sql_getTwitterKey(con):
    print("get key")
    try:
        cursorObj = con.cursor()
        print("Етсь курсор")
    except:
        print("нет курсора")
    try:
        cursorObj.execute("SELECT * FROM twitterkey")
        print("Етсь запрос")
    except Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    try:
        k = cursorObj.fetchone()
        print("Есть результат")
        print(k)
        return k

    except:
        print("Error")


def sql_select(con, row):
    try:
        cursorObj = con.cursor()
        cursorObj.execute("SELECT tweet FROM twits WHERE id = ?", row)
        twit = cursorObj.fetchone()
        print (twit)
        return twit
    except Error:
        print(Error)
