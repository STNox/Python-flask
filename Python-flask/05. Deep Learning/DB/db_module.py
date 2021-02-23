import sqlite3

def create_table(sql):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql_table = sql
    cur.execute(sql_table)
    conn.commit()
    conn.close()

def insert_status(params):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = '''insert into covid_status(
        date, region, def_cnts, local_occ, over_flow, inc_decs, death_cnts,
        isol_clr, isol_ing) values(?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()
    return

def insert_age_gender(params):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = 'insert into age_gender(date, target, confCase, confRate, criRate, death, deathRate) values(?, ?, ?, ?, ?, ?, ?);'
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()
    return

def insert_abroad(params):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = 'insert into foreign_covid(date, continent, nation, natDef, natDeath, natDeathRate) values(?, ?, ?, ?, ?, ?);'
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()
    return

def insert_seoul(params):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = 'insert into seoul(date, id_nm, dist, history, move, status) values(?, ?, ?, ?, ?, ?);'
    cur.execute(sql, params)
    conn.commit()
    cur.close()
    conn.close()
    return

def get_status(date):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = 'select * from covid_status where date=?;'
    cur.execute(sql, (date,)) # 단순 변수를 주면 튜플이나 리스트 형태로, 리스트를 변수로 주면 변수명 그대로 쓴다.
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_age_gender(date):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = 'select * from age_gender where date=?;'
    cur.execute(sql, (date,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_abroad(date):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = 'select * from foreign_covid where date=?;'
    cur.execute(sql, (date,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_capital_area():
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = "select date, inc_decs from covid_status where region in ('서울', '경기', '인천');"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_metropol():
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = "select date, inc_decs from covid_status where region in ('세종', '대전', '대구', '광주', '울산', '부산', '제주');"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_region(region):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = 'select date, inc_decs from covid_status where region=?'
    cur.execute(sql, (region,))
    rows = cur.fetchall()
    cols = [column[0] for column in cur.description]
    cur.close()
    conn.close()
    return rows, cols

def get_national_status():
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = "select date, inc_decs from covid_status where region='합계';"
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [column[0] for column in cur.description]
    cur.close()
    conn.close()
    return rows, cols

def get_seoul(date):
    conn = sqlite3.connect('./DB/covid_1.db')
    cur = conn.cursor()
    sql = 'select id_nm, dist from seoul where date=?'
    cur.execute(sql, (date,))
    rows = cur.fetchall()
    cols = [column[0] for column in cur.description]
    cur.close()
    conn.close()
    return rows, cols