from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

url = 'https://siemens.service-now.com/nav_to.do?uri=%2Fincident.do%3Fsys_id%3D8a32613787622914244db80f8bbb358e%26sysparm_record_target%3Dincident%26sysparm_record_row%3D1%26sysparm_record_rows%3D828%26sysparm_record_list%3Du_agent_updated_by%253D56fcf5cddb3e04901f74755d3b961948%255EORu_agent_updated_by%253D0e8575411b2d4c10519711331d4bcb7c%255Estate%253D6%255EORstate%253D7%255Econtact_type%253Dwalk-in%255Eu_resolver_group%253Dd313580ddb4758106f3fe7ba48961943%255EORu_resolver_group%253D7b8398750fd58240ee53c1cce1050eeb%255EORDERBYDESCsys_created_on'
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(path = r"C:\Temp\Sessoes\chromedriver").install()))
driver.get(url)
driver.switch_to.frame('gsft_main')

# links = driver.find_elements(By.TAG_NAME, "a")
# for link in links:
#     print(link.text)

# driver.find_element(By.LINK_TEXT, 'INC18351457').click()
# print(teste.text)

WebDriverWait(driver, 300).until(
    EC.text_to_be_present_in_element_value((By.ID, 'sys_readonly.incident.state'), '5')
)

# WebDriverWait(driver, 300).until(
#     EC.text_to_be_present_in_element((By.ID, 'sys_readonly.incident.state'), 'Pending')
# )

teste = driver.find_element(By.ID, 'sys_readonly.incident.state')
print(teste.text)
 
time.sleep(1000)