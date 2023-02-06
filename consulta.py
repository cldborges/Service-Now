from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

url = 'https://siemens.service-now.com'
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(path = r"C:\Temp\Sessoes\chromedriver").install()))
#alterar nas configurações do navegador para abrir a última página visitada
driver.get(url)

driver.maximize_window()

time.sleep(1000)