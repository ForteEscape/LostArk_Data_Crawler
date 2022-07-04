import datetime
import csv
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from prettytable import PrettyTable


class MarketHandler:
    def __init__(self, account_num):
        self.price_data_list = []
        self.update_time = None
        self.account, self.password = self.__get_account(account_num)
        self.item_nickname_list = self.__get_nickname()

    def __get_account(self, account_num):
        path = "./data/accounts/account_data.csv"
        account_data = None
        account = None
        password = None

        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            account_data = list(reader)

        file.close()

        if account_num == 0:
            account = account_data[0][0]
            password = account_data[0][1]
        elif account_num == 1:
            account = account_data[1][0]
            password = account_data[1][1]

        return account, password

    def __get_nickname(self):
        path = "./data/nickname/nickname.csv"

        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            nickname_data = list(reader)

        file.close()

        return nickname_data

    def get_price_data(self):
        try:
            data_price_list = self.__get_data_from_bookmark()

            if data_price_list is None:
                return

            print(self.update_time)

            self.price_data_list = self.__data_processing(data_price_list)
        except Exception as error:
            print(error)
            return

    def __get_data_from_bookmark(self):
        driver = self.__get_driver()
        sleep(2)
        driver.get('https://lostark.game.onstove.com/Market/BookMark')

        sleep(2)
        is_success = self.__log_in_process(driver)

        if not is_success:
            driver.quit()
            return None

        sleep(2)

        price_data = driver.find_element(By.XPATH, '//*[@id="tbodyItemList"]').text
        sleep(1)
        driver.find_element(By.XPATH, '//*[@id="marketList"]/div[2]/a[3]').click()

        sleep(2)
        price_data2 = driver.find_element(By.XPATH, '//*[@id="tbodyItemList"]').text

        data_price = price_data + '\n' + price_data2
        data_price_list = data_price.split('\n')

        driver.quit()

        self.update_time = datetime.datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')

        return data_price_list

    # 데이터 테이블 만드는 내부 메서드
    def __make_table(self, data_list):
        output = PrettyTable()

        output.field_names = ["이름", "전날가", "최근가", "최저가"]

        for index in data_list:
            output.add_row(index)

        return output

    # 데이터 가공
    def __data_processing(self, data_price_list):
        data_list = []
        for index in data_price_list:
            if index == '시세 확인 구매' or index == '[10개 단위 판매]' or index == '[구매 시 거래 불가]':
                pass
            else:
                for name in self.item_nickname_list:
                    if index in name:
                        index = name[0]

                data_list.append(index)

        temp_list = []
        data_2d_list = []

        for index in data_list:
            temp_list.append(index)

            if len(temp_list) == 4:
                data_2d_list.append(temp_list)
                temp_list = []

        return data_2d_list

    # 데이터 크롤링 준비 메서드
    def __log_in_process(self, driver):
        try:
            driver.find_element(By.XPATH, '//*[@id="user_id"]').send_keys(self.account)
            sleep(2)
            driver.find_element(By.XPATH, '//*[@id="user_pwd"]').send_keys(self.password)
            sleep(2)
            driver.find_element(By.XPATH, '//*[@id="idLogin"]/div[4]/button/span').click()

            return True

        except Exception as error:
            print("log in failed cause this error")
            print(error)
            return False

    # 데이터 크롤링 준비 메서드2
    def __get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920, 1080")

        # live service
        driver = webdriver.Chrome('./chromedriver' ,chrome_options=chrome_options)

        # ====================== testing service ==================================
        # service = Service(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
        # ====================== testing service end ==============================

        return driver
