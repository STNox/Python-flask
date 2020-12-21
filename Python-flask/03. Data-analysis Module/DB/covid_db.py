import requests
import pandas as pd
from DB.db_module import insert as ins
from bs4 import BeautifulSoup

def get_covid_status(start_date, end_date):
    key_fd = open('gov_data_api_key.txt', mode='r')
    govapi_key = key_fd.read(100)
    key_fd.close()

    base_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    url = f'{base_url}?ServiceKey={govapi_key}&pageNo=1&numOfRows=10&startCreateDt={start_date}&endCreateDt={end_date}'
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'xml')

    items = soup.find_all('item')
    regions, qur_rates, std_days, death_cnts, inc_decs, isol_clr_cnts, isol_ing_cnts, def_cnts, local_occ_cnts, over_flow_cnts = [], [], [], [], [], [], [], [], [], []
    for item in items:
        death_cnt = item.find('deathCnt').string if item.find('deathCnt') else ''
        def_cnt = item.find('defCnt').string if item.find('defCnt') else ''
        region = item.find('gubun').string if item.find('gubun') else ''
        inc_dec = item.find('incDec').string if item.find('incDec') else ''
        isol_clr_cnt = item.find('isolClearCnt').string if item.find('isolClearCnt') else ''
        isol_ing_cnt = item.find('isolIngCnt').string if item.find('isolIngCnt') else ''
        local_occ_cnt = item.find('localOccCnt').string if item.find('localOccCnt') else ''
        over_flow_cnt = item.find('overFlowCnt').string if item.find('overFlowCnt') else ''
        qur_rate = item.find('qurRate').string if item.find('qurRate') else ''
        std_day = ''.join(item.find('stdDay').string.split()[:-1]).replace('년', '-').replace('월', '-').replace('일', '')
        regions.append(region); qur_rates.append(qur_rate); std_days.append(std_day); death_cnts.append(death_cnt) 
        inc_decs.append(inc_dec); isol_clr_cnts.append(isol_clr_cnt); def_cnts.append(def_cnt)
        local_occ_cnts.append(local_occ_cnt); isol_ing_cnts.append(isol_ing_cnt); over_flow_cnts.append(over_flow_cnt)

    covid_status = pd.DataFrame({
        '일시': std_days,
        '지역': regions,
        '누적확진': def_cnts,
        '국내발생': local_occ_cnts,
        '해외유입': over_flow_cnts,
        '전일대비 증감': inc_decs,
        '10만명당 발생률': qur_rates,
        '사망': death_cnts,
        '격리해제': isol_clr_cnts,
        '격리중': isol_ing_cnts
    })

    covid_status = covid_status.set_index('지역')
    covid_status = covid_status.drop(['검역'])
    covid_status = covid_status.reset_index()
    
    ins(covid_status, covid_status)
    
    