import sqlite3
import sys
import traceback
from sqlite3 import Error



def sql_connection():
    try:
        con = sqlite3.connect("twitdb.db")
        print("Нормес прошло. ДБ создано")
        return con
    except Error:
        print(Error)


def sql_table(con):
    cursObj = con.cursor()
    try:
        cursObj.execute('CREATE TABLE IF NOT EXISTS twits (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, tweet text NOT NULL)')
        print("DB created")
        con.commit()
    except Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))



def sql_insert(con, twit):
    cursorObj = con.cursor()
    try:
        cursorObj.execute("INSERT INTO 'twits'('tweet')VALUES('?')", twit)
        print("Done")
        con.commit()
    except Error:
        print(Error)


def sql_getRow(con):
    cursorObj = con.cursor()
    try:
        k = cursorObj.execute("SELECT * FROM twits").rowcount
        return k
    except Error:
        print(Error)


def sql_select(con, row):
    try:
        cursorObj = con.cursor()
        twit = cursorObj.execute("SELECT tweet FROM twits WHERE id LIKES '?'", row)
        return twit
    except Error:
        print(Error)
