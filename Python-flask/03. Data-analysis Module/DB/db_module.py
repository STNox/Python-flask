import sqlite3
import pandas as pd

def create_table():
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql_table = '''create table covid_status (
        date text not null,
        region text not null,
        def_cnts int default 0,
        local_occ int default 0,
        over_flow int default 0,
        inc_decs int default 0,
        death_cnts int default 0,
        isol_clr int default 0,
        isol_ing int default 0, 
        qur_rates float default 0
    );'''
    cur.execute(sql_table)
    conn.commit()
    conn.close()

def insert(df, db_name):
    sql_insert = f'insert into {db_name} values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'
    for i in df.index:
        params = [df['일시'][i], df['지역'][i], int(df['누적확진'][i]), int(df['국내발생'][i]), int(df['해외유입'][i]), int(df['전일대비 증감'][i]), int(df['사망'][i]), int(df['격리해제'][i]), int(df['격리중'][i])]
        params.append(None if df['10만명당 발생률'][i] == '-' else float(df['10만명당 발생률'][i]))
        conn = sqlite3.connect('covid_1.db')
        cur = conn.cursor()
        cur.execute(sql_insert, params)
        conn.commit()
        conn.close()

def select(db_name):
    conn = sqlite3.connect('covid_1.db')
    cur = conn.cursor()
    sql_select = f'select * from {db_name}'
    cur.execute(sql_select)
    conn.close()