from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from datetime import date


url = 'https://siemens.service-now.com'
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(path = r"C:\Temp\Sessoes\chromedriver").install()))
#alterar nas configurações do navegador para abrir a última página visitada
driver.get(url)

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="gsft_nav"]/div/magellan-favorites-list/ul/li[3]/div/div[1]/a/div[2]/span')))
criar_novo = driver.find_element(By.XPATH, '//*[@id="gsft_nav"]/div/magellan-favorites-list/ul/li[3]/div/div[1]/a/div[2]/span')
print(criar_novo.text)
time.sleep(5)
criar_novo.click()
time.sleep(10)
driver.switch_to.frame('gsft_main')
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="label.incident.caller_id"]/label/span[2]'))) #//*[@id="sys_display.incident.caller_id"]
costumer_id = driver.find_element(By.ID, 'sys_display.incident.caller_id')
costumer_id.send_keys('z0026jjc')
time.sleep(5)
Select(driver.find_element(By.ID, 'incident.contact_type')).select_by_visible_text('Walk-in')
time.sleep(100)