import requests
import pandas as pd
from flask import current_app
from datetime import datetime
from bs4 import BeautifulSoup
from DB import db_module as dm

key_fd = open('gov_data_api_key.txt', mode='r')
govapi_key = key_fd.read(100)
key_fd.close()

def add_status(date):
    date_t = date.replace('-', '')
    base_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    url = f'{base_url}?ServiceKey={govapi_key}&pageNo=1&numOfRows=10&startCreateDt={date_t}&endCreateDt={date_t}'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'xml')

    items = soup.find_all('item')
    for item in items:
        death_cnt = int(item.find('deathCnt').string) if item.find('deathCnt') else 0
        def_cnt = int(item.find('defCnt').string) if item.find('defCnt') else 0
        region = item.find('gubun').string if item.find('gubun') else ''
        inc_dec = int(item.find('incDec').string) if item.find('incDec') else 0
        isol_clr_cnt = int(item.find('isolClearCnt').string) if item.find('isolClearCnt') else 0
        isol_ing_cnt = int(item.find('isolIngCnt').string) if item.find('isolIngCnt') else 0
        local_occ_cnt = int(item.find('localOccCnt').string) if item.find('localOccCnt') else 0
        over_flow_cnt = int(item.find('overFlowCnt').string) if item.find('overFlowCnt') else 0
        qur_rate = None
        if item.find('qurRate'):
            qur = item.find('qurRate').string
            if qur != None and qur[-1] == '.':
                qur = qur[:-1]
            if qur != None and qur[0] in '0123456789':
                qur_rate = float(qur)
        std_day = ''.join(item.find('stdDay').string.split()[:-1]).replace('년', '-').replace('월', '-').replace('일', '')
        std_day = datetime.strptime(std_day, '%Y-%m-%d')
        std_day = std_day.strftime('%Y-%m-%d')
        
        if region != '검역':
            params = [std_day, region, def_cnt, local_occ_cnt, over_flow_cnt, inc_dec, death_cnt, isol_clr_cnt, isol_ing_cnt]
            dm.insert_status(params)
    
    current_app.logger.info(f'{date} status data successfully inserted.')

def add_age_gender(date):
    date_t = date.replace('-', '')
    base_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19GenAgeCaseInfJson'
    url = f'{base_url}?ServiceKey={govapi_key}&pageNo=1&numOfRows=10&startCreateDt={date_t}&endCreateDt={date_t}'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'xml')

    items = soup.find_all('item')
    for item in items:
        confCase = int(item.find('confCase').string) if item.find('confCase') else 0
        confCaseRate = float(item.find('confCaseRate').string) if item.find('confCaseRate') else 0
        date = item.find('createDt').string.split()[0] if item.find('createDt') else ''
        cri_rate = float(item.find('criticalRate').string) if item.find('criticalRate') else 0
        death = int(item.find('death').string) if item.find('death') else 0
        deathRate = float(item.find('deathRate').string) if item.find('deathRate') else 0
        target = item.find('gubun').string if item.find('gubun') else 0

        params = [date, target, confCase, confCaseRate, cri_rate, death, deathRate]
        dm.insert_age_gender(params)
    
    current_app.logger.info(f'{date} age_gender data successfully inserted.')

def add_abroad(date):
    date_t = date.replace('-', '')
    base_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19NatInfStateJson'
    url = f'{base_url}?ServiceKey={govapi_key}&pageNo=1&numOfRows=10&startCreateDt={date_t}&endCreateDt={date_t}'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'xml')

    items = soup.find_all('item')
    for item in items:
        natDef = int(item.find('natDefCnt').string) if item.find('natDefCnt') else 0
        continent = item.find('areaNm').string if item.find('areaNm') else ''
        date = ''.join(item.find('stdDay').string.split()[:-1]).replace('년', '-').replace('월', '-').replace('일', '')
        date = datetime.strptime(date, '%Y-%m-%d')
        date = date.strftime('%Y-%m-%d')
        nation = item.find('nationNm').string if item.find('nationNm') else ''
        natDeath = int(item.find('natDeathCnt').string) if item.find('natDeathCnt') else 0
        natDeathRate = round(float(item.find('natDeathRate').string), 2) if item.find('natDeathRate') else 0

        params = [date, continent, nation, natDef, natDeath, natDeathRate]
        dm.insert_abroad(params)
    
    current_app.logger.info(f'{date} abroad data successfully inserted.')

