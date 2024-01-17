from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from funcoes import *

minimize_console_window()

url = 'https://siemens.service-now.com'
# url = 'https://siemens.service-now.com/login_with_sso.do?glide_sso_id=2786c102db3298100e1f772b68961925'
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
driver = webdriver.Chrome(options=options)
#alterar nas configurações do navegador para abrir a última página visitada
driver.get(url)

driver.maximize_window()

time.sleep(10000)