from multiprocessing import Pool
from pytz import timezone
import DataCrawling
import csv
import datetime
import schedule
import time


def createCrawler(account_num):
    path = "./data/output/"
    dataCrawler = DataCrawling.MarketHandler(account_num)
    dataCrawler.get_price_data()

    if account_num == 0:
        with open(path + "Material_data.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            for row in dataCrawler.price_data_list:
                writer.writerow(row)
        file.close()
    else:
        with open(path + "Engrave_data.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            for row in dataCrawler.price_data_list:
                writer.writerow(row)
        file.close()


def csv_integration():
    path = "./data/output/"

    with open(path + "Material_data.csv", 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        material_data = list(reader)
    file.close()

    with open(path + "Engrave_data.csv", 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for line in reader:
            material_data.append(line)
    file.close()

    with open(path + "Total_data.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        for row in material_data:
            writer.writerow(row)
    file.close()

    print("integration complete")


def start_process():
    process_pool = Pool(2)

    process_pool.map_async(createCrawler, [0, 1])
    process_pool.close()
    process_pool.join()


def chk_time():
    chk_time = datetime.datetime.now(timezone('Asia/Seoul'))

    if (chk_time.minute == 20 and chk_time.second == 0) or (chk_time.minute == 50 and chk_time.second == 0):
        start_process()
        csv_integration()


if __name__ == '__main__':
    schedule.every(1).seconds.do(chk_time)

    while True:
        schedule.run_pending()
        time.sleep(1)