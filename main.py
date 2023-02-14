from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from funcoes import *
import easygui


# costumer_id = input('Identificação do usuário: ').strip()
# linha = int(input('Qual a linha?: ') ) - 2
costumer_id = easygui.enterbox('Identificação do usuário: ').strip()
linha = int(easygui.enterbox('Qual a linha?: ') ) - 2
remoto = easygui.boolbox('É passível de remoto?')

# df = pd.read_excel('C:/Temp/teste.xlsm') 
df = pd.read_excel('C:/Users/z0026jjc/OneDrive - Atos/Base de dados dos chamados - Python.xlsm') # O arquivo precisa estar fechado, por isso uso uma cópia para consulta em tempo real
df = df.drop(['Cod_Category', 'Cod_Category2', 'Cod_Category3', 'Template', ], axis='columns')

# category = input('Categoria: ')
# subcategory = input('Subcategoria: ')
# subsubcategory = input('Subsubcategoria: ')
# short_description = input('Título: ')
# description = input('Descrição: ')
# tipo = input('Tipo: ')
# data_points = input('Identificação do usuário: ')

category = df.loc[linha, 'Category']
subcategory = df.loc[linha, 'Subcategory']
subsubcategory = df.loc[linha, 'Subsubcategory']
short_description = df.loc[linha, 'Short Description']
description = df.loc[linha, 'Description']
tipo = df.loc[linha, 'Tipo']
if pd.isnull(tipo):
    tipo = 'Incident'


url = 'https://siemens.service-now.com'
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(path = r"C:\Temp\Sessoes\chromedriver").install()))
#alterar nas configurações do navegador para abrir a última página visitada
driver.get(url)

driver.maximize_window()

WebDriverWait(driver, 80).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="gsft_nav"]/div/magellan-favorites-list/ul/li[3]/div/div[1]/a/div[2]/span')))
criar_novo = driver.find_element(By.XPATH, '//*[@id="gsft_nav"]/div/magellan-favorites-list/ul/li[3]/div/div[1]/a/div[2]/span')
print(criar_novo.text)
time.sleep(5)
criar_novo.click()
time.sleep(6)

driver.switch_to.frame('gsft_main')

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="label.incident.caller_id"]/label/span[2]'))) #//*[@id="sys_display.incident.caller_id"]
driver.find_element(By.ID, 'sys_display.incident.caller_id').send_keys(costumer_id)
time.sleep(3)
Select(driver.find_element(By.ID, 'incident.contact_type')).select_by_visible_text('Walk-in')
try:
    WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, 'incident.location_fieldmsg')))
except:
    pass

# time.sleep(30)
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.category"]/option[2]'))) #verifica se estão aparecendo mais de uma opção no Category
Select(driver.find_element(By.ID, 'sys_select.incident.category')).select_by_visible_text(category)
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.subcategory"]/option[2]'))) 
Select(driver.find_element(By.ID, 'sys_select.incident.subcategory')).select_by_visible_text(subcategory)
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.u_subsubcategory"]/option[2]')))
Select(driver.find_element(By.ID, 'sys_select.incident.u_subsubcategory')).select_by_visible_text(subsubcategory)



time.sleep(3)
driver.find_element(By.ID, 'sys_display.incident.assignment_group').clear()
time.sleep(3)
driver.find_element(By.ID, 'sys_display.incident.assignment_group').send_keys('INC_Atos_L1.5_UseIT_Center_BRAZIL')

Select(driver.find_element(By.ID, 'incident.u_type')).select_by_visible_text(tipo)

time.sleep(3)
driver.find_element(By.ID, 'sys_display.incident.assigned_to').send_keys('BORGES CLAUDIO (IT DF SIAM STG)')

driver.find_element(By.ID, 'incident.short_description').send_keys(short_description)
driver.find_element(By.ID, 'incident.description').send_keys(description)

#driver.find_element(By., '//*[@id="tabs2_section"]/span[3]/span[1]').click()

driver.find_element(By.XPATH, '//span[text()="Notes"]').click()

time.sleep(3)

try:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'incident.u_data_points')))

    dp = driver.find_element(By.ID, 'incident.u_data_points').get_attribute('value')
    dp = dp.replace('!!!', '!!!!')
    driver.find_element(By.ID, 'incident.u_data_points').clear()
    driver.find_element(By.ID, 'incident.u_data_points').send_keys(dp)
    # data_points = driver.find_element(By.ID, 'incident.u_data_points')
    # print(dp)
except:
    print('Não tem DP') 

# WebDriverWait(driver, 200).until(
#     EC.element_located_to_be_selected
# )

prosseguir = easygui.boolbox('Prosseguir com o registro do chamado?')

if prosseguir == True:
    driver.find_element(By.ID, 'sysverb_insert').click()
else:
    print(prosseguir)
    driver.quit()

time.sleep(1000)