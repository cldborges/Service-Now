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
    costumer_id = costumer_id.replace(',', '')
    linha = int(easygui.enterbox('Qual a linha?: ') ) - 2
    remoto = easygui.boolbox('É passível de remoto?')

    # TESTES
    # costumer_id = 'z0026jjc'
    # linha = 7
    # remoto = False

    if '.' in costumer_id and '@' not in costumer_id:
        costumer_id += '@siemens.com'

    # df = pd.read_excel('C:/Temp/teste.xlsm') 
    df = pd.read_excel('C:/Users/z0026jjc/OneDrive - Atos/Base de dados dos chamados - Python.xlsm') # O arquivo precisa estar fechado, por isso uso uma cópia para consulta em tempo real
    df = df.drop(['Cod_Category', 'Cod_Category2', 'Cod_Category3', 'Template', ], axis='columns')

    category = df.loc[linha, 'Category']
    subcategory = df.loc[linha, 'Subcategory']
    # if subcategory == 'DWP Win 10 Local Client':
    #     accenture = easygui.boolbox('É Accenture?')
    #     if accenture == True:
    #         subcategory = f'Accenture {subcategory}'
    subsubcategory = df.loc[linha, 'Subsubcategory']
    categorization = df.loc[linha, 'Categorization']
    categorization_bool = True
    if pd.isnull(categorization):
        # categorization = easygui.enterbox('Qual o Categorization?')
        categorization = f'{category} / {subcategory} / {subsubcategory}'
        if categorization == 'nan / nan / nan':
            categorization_bool = False
        else:
            categorization_bool = easygui.boolbox(f'Categorization vazio, deseja usar a categorização antiga? - {categorization}')
        

    # if categorization == None:
    #     categorization = f'{category} / {subcategory} / {subsubcategory}'

    # categorization = 'Collaboration / MobileIT / Android'
    short_description = df.loc[linha, 'Short Description']
    short_description = '#UIT - ' + short_description
    description = df.loc[linha, 'Description']
    tipo = df.loc[linha, 'Tipo']
    if pd.isnull(tipo):
        tipo = 'Incident'
    resolucao = df.loc[linha, 'Resolução']
    if pd.isnull(resolucao):
        resolucao = df.loc[linha, 'Resolução-ing']

    # url = 'https://siemensfuturenowprod.service-now.com/partner'
    # url = 'https://siemensfuturenowprod.service-now.com/now/nav/ui/home'
    url = 'https://siemensfuturenowprod.service-now.com/incident.do?sys_id=-1&sysparm_query=active=true&sysparm_stack=incident_list.do?sysparm_query=active=true'
    options = webdriver.ChromeOptions()
    # options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
    # driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(path = r"C:\Temp\Sessoes\chromedriver").install()))
    options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
    driver = webdriver.Chrome(options=options)
    # IMPORTANTE - alterar nas configurações do navegador para abrir a última página visitada
    driver.get(url)
    driver.maximize_window()
    # time.sleep(10)
    # WebDriverWait(driver, 80).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="gsft_nav"]/div/magellan-favorites-list/ul/li[3]/div/div[1]/a/div[2]/span')))
    # botão criar novo
    # criar_novo = driver.find_element(By.CSS_SELECTOR, '#ae2afe6993e3b510fbaf7c9efaba1063 > span > span')
    # criar_novo = driver.find_element(By.LINK_TEXT, 'Criar novo')
    # criar_novo = driver.find_element(By.XPATH, '//*[@id="gsft_nav"]/div/magellan-favorites-list/ul/li[3]/div/div[1]/a/div[2]/span')
    # print(criar_novo.text)
    # time.sleep(5)
    # criar_novo.click()
    # time.sleep(6)

    # driver.switch_to.frame('gsft_main')

    # WebDriverWait(driver, 20).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="label.incident.caller_id"]/label/span[2]'))) #//*[@id="sys_display.incident.caller_id"]
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, r'#label\.incident\.location > label > span.label-text'))) #//*[@id="sys_display.incident.caller_id"]
    # time.sleep(3)
    driver.find_element(By.ID, 'sys_display.incident.caller_id').send_keys(costumer_id) 
    time.sleep(3)
    Select(driver.find_element(By.ID, 'incident.contact_type')).select_by_visible_text('Walk-in')
    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'incident.location_fieldmsg')))
    except:
        pass

    # try: 
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.category"]/option[2]'))) #verifica se estão aparecendo mais de uma opção no Category
    # except:
    #      raise GIDInvalido('GID inválido')
    # Select(driver.find_element(By.ID, 'sys_select.incident.category')).select_by_visible_text(category)
    # WebDriverWait(driver, 15).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.subcategory"]/option[2]'))) 
    # Select(driver.find_element(By.ID, 'sys_select.incident.subcategory')).select_by_visible_text(subcategory)
    # try:
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.u_subsubcategory"]/option[2]')))
    #     Select(driver.find_element(By.ID, 'sys_select.incident.u_subsubcategory')).select_by_visible_text(subsubcategory)
    # except:
    #     subcategory = 'DWP Win 10 Local Client'
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.subcategory"]/option[2]'))) 
    #     Select(driver.find_element(By.ID, 'sys_select.incident.subcategory')).select_by_visible_text(subcategory)
    #     # time.sleep(3)
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@id="sys_select.incident.u_subsubcategory"]/option[2]')))
    #     Select(driver.find_element(By.ID, 'sys_select.incident.u_subsubcategory')).select_by_visible_text(subsubcategory)
    if categorization_bool == True:
    # if categorization != None:
        driver.find_element(By.ID, 'sys_display.incident.u_categorization').send_keys(categorization)
        time.sleep(5)

        driver.find_element(By.CSS_SELECTOR, r'#label\.incident\.u_categorization > label > span.label-text').click()
    else:
        easygui.msgbox('Preencha o Categorization e aperte o OK')
    time.sleep(5)
    callback = driver.find_element(By.ID, 'incident.u_callback_number')
    callback_txt = callback.get_attribute('value')
    if callback_txt == '':
        callback.send_keys('TEAMS')
        
    # elem_categorization = driver.find_element(By.ID, 'sys_display.incident.u_categorization')
    # elem_categorization.send_keys(categorization)
    # elem_categorization.click()

    
    time.sleep(3)
    Select(driver.find_element(By.ID, 'incident.u_type')).select_by_visible_text(tipo)

    time.sleep(3)
    driver.find_element(By.ID, 'sys_display.incident.assignment_group').clear()
    time.sleep(3)
    driver.find_element(By.ID, 'sys_display.incident.assignment_group').send_keys('INC_Atos_L1.5_UseIT_Center_BRAZIL')



    time.sleep(3)
    # driver.find_element(By.ID, 'sys_display.incident.assigned_to').send_keys('Borges Claudio Ferreira (RC-BR IT UIT)')
    # driver.find_element(By.ID, 'sys_display.incident.assigned_to').send_keys('Borges, Claudio Ferreira (ext) (RC-BR IT UIT)')
    driver.find_element(By.ID, 'sys_display.incident.assigned_to').send_keys('Borges, Claudio Ferreira (BP) (RC-BR IT UIT)')

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
    
    # verificar se precisa preencher a tradução e seleciona caso precise
    translation = driver.find_element(By.CSS_SELECTOR, '#tabs2_section > span:nth-child(10) > span.tabs2_tab.default-focus-outline > span.label_description')
    # translation = driver.find_element(By.CSS_SELECTOR, '#tabs2_section > span:nth-child(4) > span.tabs2_tab.default-focus-outline > span.label_description')
    print(translation.text)
    if translation.text == '*':
        translation.click()
        Select(driver.find_element(By.ID, 'incident.u_user_language')).select_by_visible_text('Portuguese')


    prosseguir = easygui.boolbox('Prosseguir com o registro do chamado?')

    relatorio(tipo, remoto)

    if prosseguir == True:
        inc = driver.find_element(By.ID, 'sys_readonly.incident.number').get_attribute('value')
        print(inc)
        driver.find_element(By.ID, 'sysverb_insert').click()
        
        # # entrar no incidentes abertos para mim
        # # time.sleep(5)
        # driver.switch_to.default_content()
        # WebDriverWait(driver, 60).until(
        #     EC.element_to_be_clickable((By.LINK_TEXT, 'Assigned to me')))
        # driver.find_element(By.LINK_TEXT, 'Assigned to me').click()
        # driver.switch_to.frame('gsft_main')
        # # driver.find_element(By.CSS_SELECTOR, 'gsft_nav > div > magellan-favorites-list > ul > li:nth-child(5) > div > div:nth-child(1) > a > div:nth-child(2) > span').click()
        # # assignados_para_mim.click()

        WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.LINK_TEXT, inc)))
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, inc).click()
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Resolution Information"]')))
        driver.find_element(By.XPATH, '//span[text()="Resolution Information"]').click()
        # time.sleep(10)
        Select(driver.find_element(By.ID, 'incident.close_code')).select_by_visible_text('Solved (Permanently)')
        if resolucao != 'nan':
            driver.find_element(By.ID, 'incident.close_notes').send_keys(resolucao)

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