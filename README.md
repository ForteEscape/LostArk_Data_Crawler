# LostArk_Data_Crawler

## 1. 해당 프로젝트 소개
- LostArk_Data_Crawler 는 LOA_HELP_BOT 이 이전 직접 진행하던 거래소 가격 데이터 크롤링 업무를 대신하여
서버 벡그라운드에 동작하도록 하는 일종의 배치(batch) 프로그램입니다.

## 2. 해당 프로젝트 구성
- 크롤링 업무만 이관받아 진행하는 프로그램인 만큼 구성은 매우 간단하며 실질적 구동부인 main.py와 크롤링 및 데이터
처리 관련을 담당하는 DataCrawling.py 가 존재합니다.

## 3. 설명
- main.py의 경우 대한민국 표준시(UTC+9) 기준으로 매 시간 20분과 50분에 로스트아크 거래소 데이터 크롤링 업무를
시작합니다. 2022-07-05 00:41분 기준 2개 프로세스가 동시에 병렬로 거래소 데이터 크롤링을 진행하며 크롤링한 데이터를
데이터파일로 저장하며 병렬로 저장된 데이터파일을 합처 최종 데이터파일을 만드는 역할을 담당합니다.
<br></br>
- DataCrawling.py는 LOA_HELP_BOT 의 MarketHandler.py에서 디스코드 관련 모듈을 제외하고 데이터 크롤링 모듈
만 따로 모아 재구성한 클래스파일로 데이터 크롤링 및 데이터파일로 구성하는 업무를 담당합니다.
<br></br>
- main에서는 오직 해당 클래스의 ```get_price_data()``` 으로만 클래스와 통신이 가능하며 해당 함수의 결과로
```./data``` 경로에 데이터파일이 생성됩니다.

## 4. 라이센스
- 해당 프로젝트 라이센스는 MIT 라이센스가 적용됩니다.

----------------------------------------

# LostArk_Data_Crawler

## 1. Project Introduce
- LostArk_Data_Crawler takes the place of LOA_HELP_BOT's previous exchange price data crawling work.
It is a kind of batch program that runs in the server background.

## 2. Project configuration
- As it is a program that transfers only crawling tasks, the configuration is very simple, and the main.py, which is the actual driving unit, and crawling and data
There is DataCrawling.py responsible for processing.

## 3. Project Description
- In the case of main.py, the LostArk market data(LostArk KOR) crawling task is performed at 20 and 50 minutes every hour based on Korean Standard Time (UTC+9).
Start. As of 2022-07-05 00:41, two processes crawl the market data in parallel at the same time and collect the crawled data.
It is saved as a data file and is responsible for creating the final data file by merging the data files stored in parallel.
<br></br>
- DataCrawling.py is a data crawling module except for Discord related modules in MarketHandler.py of LOA_HELP_BOT
It is responsible for crawling data and composing it into a data file with a class file that is collected and reconstructed separately.
<br></br>
- In main, communication with the class is possible only with ```get_price_data()``` of the class, and the result of the function is
created in the ```./data``` path.

## 4. License
- The project license is governed by the MIT License.