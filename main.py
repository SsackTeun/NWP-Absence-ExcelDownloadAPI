import os
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from flask import Flask, send_file, render_template, request
from datetime import datetime
import calendar


app = Flask(__name__)

download_path = os.path.join(os.getcwd(), 'my_downloads')
file_path = download_path+"\\absenceTimeOffList.xlsx"  # 실제 파일 경로로 변경
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download')
def download_file():
    date = request.args.get('date', '')
    print('date : ' + date)
    getabsenceTimeOffList(date)
    return send_file(file_path, as_attachment=True)

def getabsenceTimeOffList(date):
    # 날짜 형식으로 변환
    input_date = datetime.strptime(date, "%Y%m")

    # 해당 월의 첫 번째 날
    first_day = input_date.strftime("%Y.%m.%d")

    # 해당 월의 마지막 날짜를 계산
    last_day_num = calendar.monthrange(input_date.year, input_date.month)[1]
    last_day = datetime(input_date.year, input_date.month, last_day_num).strftime("%Y.%m.%d")

    # 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--headless")  # 헤드리스 모드 활성화
    chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화
    chrome_options.add_argument("--no-sandbox")  # 샌드박스 모드 비활성화
    chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 비활성화
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,  # 다운로드 프롬프트 비활성화
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })



    # 근태페이지 이동
    url = "https://onware.ncpworkplace.com/hrs/manager/absence/timeOffList"
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)

    # 로그인 안되있을시 로그인 페이지
    credentials = {}
    with open("credential.txt", "r") as f:
        for line in f:
            key, value = line.strip().split('=')
            credentials[key] = value

    username = credentials['username']
    password = credentials['password']

    driver.find_element(By.ID, 'user').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'loginBtn').click()

    time.sleep(3)

    select_searchFromYmd = driver.find_element(By.ID, 'hiddenFromYmd')
    driver.execute_script(f"arguments[0].setAttribute('value', '{first_day}')", select_searchFromYmd)


    select_searchToYmd = driver.find_element(By.ID, 'hiddenToYmd')
    driver.execute_script(f"arguments[0].setAttribute('value', '{last_day}')", select_searchToYmd)

    updated_value_from = driver.execute_script("return arguments[0].getAttribute('value')", select_searchFromYmd)
    print("Updated From Date:", updated_value_from)

    updated_value_to = driver.execute_script("return arguments[0].getAttribute('value')", select_searchToYmd)
    print("Updated To Date:", updated_value_to)

    # JavaScript 코드 실행
    # jQuery 코드를 순수 JavaScript로 변환하여 실행
    js_code = f"""
    $("input[name='searchFromYmd']").val("{first_day}");
    $("input[name='searchToYmd']").val("{last_day}");
    document.querySelector('#searchForm').setAttribute('action', '/hrs/manager/absence/download');
    document.querySelector('#searchForm').submit();
    """
    driver.execute_script(js_code)


if __name__ == '__main__':
    app.run(debug=True)