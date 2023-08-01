# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from funcoes import *
import easygui

minimize_console_window()

# Ler credenciais
try:
    usuario, senha = ler_credenciais()
except:
    atualizar_credenciais()
    usuario, senha = ler_credenciais()

def login():
    url = 'https://siemens.service-now.com'
    options = webdriver.ChromeOptions()
    # options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
    # driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager(path = r"C:\Temp\Sessoes\chromedriver").install()))
    options.add_argument(r'--user-data-dir=C:/Temp/Sessoes/UserData/') #caso dê erros com o caminho, principalmente quando termina com \, alterar as barras para /
    driver = webdriver.Chrome(options=options)
    #alterar nas configurações do navegador para abrir a última página visitada
    driver.get(url)
    driver.maximize_window()
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, '1-email')))
    driver.find_element(By.ID, '1-email').send_keys('c@atos.net')
    driver.find_element(By.NAME, 'submit').click()
    button = driver.find_element(By.XPATH, '//button[text()="AUTH"]').click()
    driver.find_element(By.NAME, 'com.siemens.dxa.applications.web.authn.challenging.username').send_keys('A402958')
    driver.find_element(By.NAME, 'com.siemens.dxa.applications.web.authn.challenging.response').send_keys(senha)
    token = easygui.enterbox('Digite o token: ')
    driver.find_element(By.NAME, 'com.siemens.dxa.applications.web.authn.challenging.response2').send_keys(token)
    driver.find_element(By.CLASS_NAME, 'btn-block').click()
    return driver


driver = login()

try:
    erro = WebDriverWait(driver, 10).until(
        EC.title_is('An error occurred'))
    print(erro)
    # erro = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.LINK_TEXT, 'body > h1'))).text
    if erro == True:
        driver.quit()
        login()
except:
    pass
    
    
WebDriverWait(driver, 80).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="gsft_nav"]/div/magellan-favorites-list/ul/li[3]/div/div[1]/a/div[2]/span')))
driver.quit()