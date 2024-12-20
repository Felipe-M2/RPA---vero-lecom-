from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

class scraping:
    def __init__(self):  
        service = Service('./chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
    
    # Leitura do arquivo JSON
    with open('./data.json', 'r', encoding='utf-8') as data:
        dados = json.load(data)
        
    result = {}
    
    
    
    #Config
        
    def abrir_site(self):
        self.driver.get(os.getenv('SITE'))
        self.usuario = os.getenv('USUARIO')
        self.senha = os.getenv('SENHA')
        time.sleep(2)
        self.loguin()

    def loguin(self):
        try:        
            waitDriver = wdWait(self.driver, 10)
            
            #USUARIO
            waitDriver.until(EC.presence_of_element_located((By.CLASS_NAME, 'ant-input-lg'))).send_keys(self.usuario)
            
            waitDriver.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ant-btn-primary'))).click()
            
            #SENHA
            time.sleep(1)
            waitDriver.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))).send_keys(self.senha)
            
            waitDriver.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ant-btn-primary'))).click()
            
            
        except TimeoutException:
            print('O elemento demorou muito para carregar!')
        except NoSuchElementException:
            print('O elemento não foi encontrado!')
        finally:
            self.buscar_dados()
    
    #Busca dados após o loguin
    def buscar_dados(self):
        try:
            time.sleep(2)
            botao_prox = self.driver.find_element(By.CLASS_NAME, 'ant-btn-primary').click()
            
            time.sleep(2)
            
            #faz uma verificação para cada iten do JSON
            for data in self.dados:
                cpf = data.get('cpf')
                contrato = data.get('contrato')
                
                self.driver.find_element(By.CLASS_NAME, 'ant-input-lg').click()
                
                time.sleep(2)
                self.driver.find_element(By.CLASS_NAME, 'ant-select-selection__rendered').click()
                
                time.sleep(2)
                self.driver.find_element(By.CLASS_NAME, 'ant-select-search__field').send_keys('Solicitação de Mudança de Endereço V3')
                
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//li[contains(text(), "Solicitação de Mudança de Endereço V3")]').click()
                
                time.sleep(1)
                self.driver.find_element(By.XPATH, '//input[@maxlength="18"]').send_keys(cpf)
                
                time.sleep(1)
                self.driver.find_element(By.CLASS_NAME, 'ant-input-number-input').send_keys(contrato)
                
                time.sleep(1)
                self.driver.find_element(By.CLASS_NAME, 'button-search').click() 

                time.sleep(2)
                num_codigo_scraping = self.driver.find_elements(By.XPATH, '//a[contains(@class, "col-with-link")]')
            
                if num_codigo_scraping:
                    href_cod = num_codigo_scraping[0].get_attribute('href')
                    cod_num = href_cod.split('/')[-1]
                
                    status_scraping = self.driver.find_element(By.CLASS_NAME, 'tag-process-status-progress')
                    status = status_scraping.text
                    
                    self.result[contrato] = {
                        "cpf": cpf,
                        "codigo": cod_num,
                        "status": status
                    }
                else:
                    self.result[contrato] = {
                        "cpf": cpf,
                        "codigo": False,
                        "status": False
                    }
        except TimeoutException:
            print("O elemento demorou muito para carregar!")
        except NoSuchElementException:
            print('O elemento não foi encontrado')
        finally:
            try:
                with open('resultado.json', 'w', encoding='utf-8') as arquivo:
                    json.dump(self.result, arquivo, ensure_ascii=False, indent=4)
            except:
                return f'Erro: {KeyError}'
iniciar = scraping()
iniciar.abrir_site()