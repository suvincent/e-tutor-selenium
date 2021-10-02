# e-Tutor 爬蟲成績
## Get Started

(1st-time) Initialize Python Virtual Environment & PIP Modules
- `$ python3 -m venv py-venv`
- `$ source ./py-venv/bin/activate`
- `$ pip3 install -r requirements.txt`
- `$ deactivate`

Afterward, always run your program in Python Virtual Environment
* in linux, mac os
    - `$ source ./py-venv/bin/activate`

* in windows
    - `Set-ExecutionPolicy Unrestricted -Scope Process`
    - `.\py-venv\Scripts\activate`


## Selenium 使用要求
* 電腦有chrome瀏覽器
* 在首層資料夾中放入webdriver.exe
    * ex. [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## 程式執行
* 設定E-tutor帳密
* 設定要爬的作業網頁
* 執行 main.py, 並在15秒內通過recapcha(機器人很難通過)