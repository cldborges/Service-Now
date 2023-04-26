from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

url = 'https://siemens.service-now.com/nav_to.do?uri=%2Fincident_list.do%3Fsysparm_query%3Dactive%3Dtrue'
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(path = r"C:\Temp\Sessoes\chromedriver").install()))
driver.get(url)
driver.switch_to.frame('gsft_main')

# links = driver.find_elements(By.TAG_NAME, "a")
# for link in links:
#     print(link.text)

driver.find_element(By.LINK_TEXT, 'INC18351457').click()
# print(teste.text)

time.sleep(100)