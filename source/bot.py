"""
description : bot 클래스 : 크롤링하고 알람까지 하는 클래스. 관리자.
manager클래스다. 메인에선 그냥 이 클래스의 함수만 실행시키면 된다.
"""
# from my_alerter import Alerter
import json
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class Bot():
    def __init__(self):
        self.crawl_site = 'https://coronamask.kr/'
        self.json_file = './data/coronamask.json'
        self.mask_list = {}     # 크롤링할 마스크 사이트 정보 {name: {content, link, sell_time}}

        pass
        
    ## 크롤링 메소드
    def crawling(self, _time = 60, _count = -1):

        ## 브라우저 열기
        driver = self.open_browser(self.crawl_site)

        ## 마스크 리스트 초기화
        self.init_mask_list(driver)

        ## 마스크 정보 저장하기
        self.save_update_to_json()

        ##TODO 아침 06:00마다 마스크 리스트 정보 업데이트하기






        ## 잘 돌아가나 test
        print(self.mask_list)
        pass

    ## 판매 시간 10분전인지 체크하기
    def is_time_to_alert(self, mask):
        
        ## 한국의 현재 시간 가져오기
        



        pass

    ## mask_list를 json에 저장
    ## 게릴라판매는 직접 json만 수정하면 될수있도록하기위함
    def save_update_to_json(self):
        with open(self.json_file, 'w', encoding='utf-8') as _json_file:
            json.dump(self.mask_list, _json_file, ensure_ascii=False, indent = "\t")
    
    ## coronamask.kr을 긁어서 필요한 데이터만 파싱
    def parse_datas(self):
        pass

    ## raw data 단일 element를 받아 dictionary형태로 반환
    def get_data_dictionary(self, _raw_data):
        raw_str = _raw_data.find('div').get_text()

        ## 구매 불가능한 상태면 return None
        available = _raw_data.select('div > p')[1].get_text().strip()
        if available == "판매종료" : return None


        ## 정규식 이용하여 속성 알아내기
        m = re.match(r'\[(.+)\](.+)', raw_str)
        name = m.group(1)
        context = m.group(2)
        link = _raw_data.find('a').get('href')
        sell_time = re.search(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}', available)
        if sell_time : sell_time = sell_time.group()
        # date = datetime.strptime(match.group(), '%Y-%m-%d').date()
        # dic = {name:{'context':context, 'link':link}}

        dic = {name:{'context':context, 'link':link, 'sell_time':sell_time}}
        return dic

        ## 그냥 str.split이용
        # e = raw_str.find(']')
        # name = raw_str[1:e]
        # context = raw_str[e+1:]


    ## mask_list 초기화
    ## bot 생성시 / 하루 한번만 실행
    def init_mask_list(self, _driver):
        ## soup 가져오기
        html, soup = self.get_html(_driver)

        ## 필요한 정보가 담긴 wrapper 가져오기
        raw_data = soup.select('.pb-14 > div:nth-child(1) > div:nth-child(1) > div.w-full > div:nth-child(2)')

        for data in raw_data:
            d = self.get_data_dictionary(data)
            if d : self.mask_list = {**self.mask_list, **self.get_data_dictionary(data)}



        ##TODO raw_data에서 판매 시간 뽑기


        pass

    ## 웹페이지 열기
    def open_browser(self, _link):
        ##TODO headless browser로 바꾸기
        driver = webdriver.Chrome('./assets/chromedriver_win32/chromedriver.exe')
        driver.set_page_load_timeout(60)
        driver.get(_link)
        return driver

    ## 페이지의 내용을 조작할수 있게 html과 bs4 결과를 리턴
    def get_html(self, _driver):
        html = _driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return html, soup

"""==============================================="""
 ## 크롤링할 사이트 브라우저로 열고 (commu,driver) 튜플 리턴
    # def open_browser(self, commu, _key):

    #     options = webdriver.ChromeOptions()
    #     options.add_argument('headless')
    #     options.add_argument('window-size=1920x1080')
    #     options.add_argument('no-sandbox')
    #     options.add_argument("disable-gpu")
    #     options.add_argument('autoplay-policy=no-user-gesture-required')
    #     options.add_argument("disable-features=AutoplayIgnoreWebAudio")
    #     options.add_argument("disable-features=PreloadMediaEngagementData,AutoplayIgnoreWebAudio, MediaEngagementBypassAutoplayPolicies")
    #     options.add_argument("log-level=2") ##사이트 로그 안 보기

    #     ## headless chrome으로 돌린다
    #     driver = webdriver.Chrome('./assets/chromedriver_win32/chromedriver.exe', options=options)
    #     # driver = webdriver.Chrome('./assets/chromedriver_win32/chromedriver.exe')

    #     driver.set_page_load_timeout(15)
    #     driver.get(commu['link'])
    #     return (_key,driver)