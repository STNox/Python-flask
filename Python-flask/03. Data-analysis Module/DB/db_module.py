import sqlite3
import pandas as pd

def create_table(sql):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql_table = sql
    cur.execute(sql_table)
    conn.commit()
    conn.close()

def insert(df, sql, params):
    sql_insert = sql
    params = params
    for i in df.index:
        conn = sqlite3.connect('./DB/covid_1.db')
        cur = conn.cursor()
        cur.execute(sql_insert, params)
        conn.commit()
        conn.close()

def get_status(date):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql_select = f'select * from covid_status where date=?;'
    cur.execute(sql_select, (date,)) # 단순 변수를 주면 튜플이나 리스트 형태로, 리스트를 변수로 주면 변수명 그대로 쓴다.
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows