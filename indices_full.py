from email import header
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests 
import csv
import time 
from time import sleep
import pyautogui
import pyperclip
from attr import attr


################   FAZ SCREENSHOT DO INDICE TJLP NO SITE DO BNDES #################
pyautogui.PAUSE = 1

pyautogui.press ("win")
pyautogui.PAUSE = 2.5
pyautogui.hotkey ("enter")
pyautogui.PAUSE = 2.5

#pyautogui.hotkey("ctrl","t")

pyperclip.copy("https://www.bndes.gov.br/wps/portal/site/home/financiamento/guia/custos-financeiros/taxa-juros-longo-prazo-tjlp")
pyautogui.hotkey("ctrl","v")
pyautogui.PAUSE = 7
pyautogui.press("enter")
pyautogui.PAUSE = 7
im1 = pyautogui.screenshot()
im2 = pyautogui.screenshot('TJLP_SCREEN.png')
print("################## SCREENSHOT TJLP FEITO COM SUCESSO ###################")

#################### DATA DOLAR PARA INDICES NO ARQUIVO CSV ################################

headers = {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 102.0.5005.115 Safari/537.36'}
#faz requisição no site de cotção
driver=requests.get("https://valorinveste.globo.com/cotacoes/dolar/")
soup4 = BeautifulSoup (driver.content, 'html.parser')
data= soup4.find_all(f'div',attrs={'class':'cell last-update-time-cell-desktop'})[0]


######################## BAIXA A TABELA DO IGPM ########################################
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
servico=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico,chrome_options=options, executable_path="./chromedriver")
#driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 102.0.5005.115 Safari/537.36'})
print(driver.execute_script("return navigator.userAgent;"))
##url de busca
driver.get("https://portalibre.fgv.br/sites/default/files/2022-10/igp-m_fgv_complemento_out22_0.xls")
time.sleep(2)
driver.close()

print("################## DOWNLOUD TABELA IGPM FEITO COM SUCESSO 3#################")

###################### COTAÇÃO IPCA ########################################

headers = {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 102.0.5005.115 Safari/537.36'}
#faz requisição no site de cotção
driver=requests.get("https://www.valor.srv.br/indices/ipca.php")
#print(page.content)

#faz o parser do texto HTML

soup1 = BeautifulSoup (driver.content,'html.parser')
#encontra o elemento atraves do CSS e class na pagina

ipca= soup1.find_all('td',attrs={'title':'IPCA de Setembro de 2022: -0.2900000000000000%'})[0]
#data= soup.find_all(f'div',attrs={'class':'cell last-update-time-cell-desktop'})[0]

print(ipca.text)
f= open("cotação.csv","a", newline="")
writer=csv.writer(f, delimiter=",")
writer.writerow(["\n"+'indice IPCA:',ipca.text,data.text])
f.close()

#################################   COTAÇÃO DO IENE ###################################################


driver2=requests.get("https://br.search.yahoo.com/search?fr=mcafee&type=E211BR105G0&p=iene+hoje")


#faz o parser do texto HTML

soup3 = BeautifulSoup (driver2.content,'html.parser')
#encontra o elemento atraves do CSS e class na pagina
# print(soup.text)
valor1 = soup3.find_all('td',class_='tdMain td1 fc-obsidian last')[0]

#printa a cotação do dolar no console
print(valor1.text)

#cria arquivo csv ou adiciona uma nova cotação do Iene no arquivo 
f= open("cotação.csv", "a", newline="")
writer=csv.writer(f, delimiter=",")
writer.writerow(['cotacao Iene:',valor1.text,data.text])
time.sleep(2)
f.close()




#faz requisição no site de cotção
driver7=requests.get("https://www.taxaselic.com/index.html")
#print(page.content)

#faz o parser do texto HTML

soup4 = BeautifulSoup (driver7.content, 'html.parser')
#encontra o elemento atraves do CSS e class na pagina

valor2= soup4.find_all('p',class_= 'w3-margin w3-jumbo font-bree-serif')[0]

#printa a cotação do dolar no console
print(valor2.text)

#cria arquivo csv ou adiciona um indice selic no arquivo 
f= open("cotação.csv", "a", newline="")
writer=csv.writer(f, delimiter=",")
writer.writerow(['indice Selic:',valor2.text,data.text])
time.sleep(2)
f.close()
    
##################### COTAÇÃO DO DOLAR ##########################

headers = {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 102.0.5005.115 Safari/537.36'}
#faz requisição no site de cotção
driver=requests.get("https://valorinveste.globo.com/cotacoes/dolar/")

#faz o parser do texto HTML

soup4 = BeautifulSoup (driver.content, 'html.parser')
#encontra o elemento atraves do CSS e class na pagina

valor= soup4.find_all("span",class_= "tabela-data__ticker__lastQuote")[0]
data= soup4.find_all(f'div',attrs={'class':'cell last-update-time-cell-desktop'})[0]

#printa a cotação do dolar no console
print(valor.text)

#cria arquivo csv ou adiciona uma nova cotação do dolar no arquivo 
f= open("cotação.csv", "a", newline="")
writer=csv.writer(f, delimiter=",")
writer.writerow(['cotacao Dolar:',valor.text,data.text])
time.sleep(2)
f.close()

driver.close()
