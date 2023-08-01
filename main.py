# from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
from funcoes import *
from classes import *
import easygui


minimize_console_window()

try:
    costumer_id = easygui.enterbox('Identificação do usuário: ').strip()
    linha = int(easygui.enterbox('Qual a linha?: ') ) - 2
    remoto = easygui.boolbox('É passível de remoto?')

    # df = pd.read_excel('C:/Temp/teste.xlsm') 
    df = pd.read_excel('C:/Users/z0026jjc/OneDrive - Atos/Base de dados dos chamados - Python.xlsm') # O arquivo precisa estar fechado, por isso uso uma cópia para consulta em tempo real
    df = df.drop(['Cod_Category', 'Cod_Category2', 'Cod_Category3', 'Template', ], axis='columns')

    category = df.loc[linha, 'Category']
    subcategory = df.loc[linha, 'Subcategory']
    if subcategory == 'DWP Win 10 Local Client':
        accenture = easygui.boolbox('É Accenture?')
        if accenture == True:
            subcategory = f'Accenture {subcategory}'
    subsubcategory = df.loc[linha, 'Subsubcategory']
    short_description = df.loc[linha, 'Short Description']
    description = df.loc[linha, 'Description']
    tipo = df.loc[linha, 'Tipo']
    if pd.isnull(tipo):
        tipo = 'Incident'

    url = 'https://siemens.service-now.com'
    options = webdriver.ChromeOptions()
    # options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
    # driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(path = r"C:\Temp\Sessoes\chromedriver").install()))
    options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
    driver = webdriver.Chrome(options=options)
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
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'incident.location_fieldmsg')))
    except:
        pass

    try: 
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.category"]/option[2]'))) #verifica se estão aparecendo mais de uma opção no Category
    except:
         raise GIDInvalido('GID inválido')
    Select(driver.find_element(By.ID, 'sys_select.incident.category')).select_by_visible_text(category)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.subcategory"]/option[2]'))) 
    Select(driver.find_element(By.ID, 'sys_select.incident.subcategory')).select_by_visible_text(subcategory)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.u_subsubcategory"]/option[2]')))
        Select(driver.find_element(By.ID, 'sys_select.incident.u_subsubcategory')).select_by_visible_text(subsubcategory)
    except:
        subcategory = 'DWP Win 10 Local Client'
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.subcategory"]/option[2]'))) 
        Select(driver.find_element(By.ID, 'sys_select.incident.subcategory')).select_by_visible_text(subcategory)
        # time.sleep(3)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.u_subsubcategory"]/option[2]')))
        Select(driver.find_element(By.ID, 'sys_select.incident.u_subsubcategory')).select_by_visible_text(subsubcategory)

    time.sleep(3)
    driver.find_element(By.ID, 'sys_display.incident.assignment_group').clear()
    time.sleep(3)
    driver.find_element(By.ID, 'sys_display.incident.assignment_group').send_keys('INC_Atos_L1.5_UseIT_Center_BRAZIL')

    Select(driver.find_element(By.ID, 'incident.u_type')).select_by_visible_text(tipo)

    time.sleep(3)
    driver.find_element(By.ID, 'sys_display.incident.assigned_to').send_keys('BORGES CLAUDIO (IT DF SIAM GOV)')

    driver.find_element(By.ID, 'incident.short_description').send_keys(short_description)
    driver.find_element(By.ID, 'incident.description').send_keys(description)

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

    prosseguir = easygui.boolbox('Prosseguir com o registro do chamado?')

    relatorio(tipo, remoto)

    if prosseguir == True:
        inc = driver.find_element(By.ID, 'sys_readonly.incident.number').get_attribute('value')
        print(inc)
        driver.find_element(By.ID, 'sysverb_insert').click()
        WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.LINK_TEXT, inc)))
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, inc).click()
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Closure Information"]')))
        driver.find_element(By.XPATH, '//span[text()="Closure Information"]').click()
        # time.sleep(10)
        Select(driver.find_element(By.ID, 'incident.close_code')).select_by_visible_text('Solved (Permanently)')

    else:
        print(prosseguir)
        driver.quit()

    # time.sleep(1000)

    #verifica se o "State" está como 'Resolved'
    WebDriverWait(driver, 1000).until(
        EC.text_to_be_present_in_element_value((By.ID, 'sys_readonly.incident.state'), '6')) # '6' não é o texto apresentado, é o atributo value da opção escolhida
except Exception as e:
    print("Ocorreu um erro:", str(e))
    easygui.exceptionbox("Ocorreu um erro:", str(e))