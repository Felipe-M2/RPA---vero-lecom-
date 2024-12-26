from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from datetime import date
import os
import time

load_dotenv()
router = FastAPI()

class scraping:
    def __init__(self):  
        service = Service('./chromedriver.exe')
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
    
    #Config------------------------------
    def abrir_site(self, data):
        self.driver.get(os.getenv('SITE'))
        self.usuario = os.getenv('USUARIO')
        self.senha = os.getenv('SENHA')
        time.sleep(2)
        self.loguin(data)

    def loguin(self, data):
        try:        
            waitDriver = wdWait(self.driver, 10)
            
            #USUARIO------------------------------
            waitDriver.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'ant-input-lg')
            )).send_keys(self.usuario)
            
            waitDriver.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'ant-btn-primary')
            )).click()
            
            #SENHA------------------------------
            time.sleep(1)
            waitDriver.until(EC.presence_of_element_located(
                (By.XPATH, '//input[@type="password"]')
            )).send_keys(self.senha)
            
            waitDriver.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'ant-btn-primary')
            )).click()
            
            self.abrir_formulario(data)
        except TimeoutException:
            return f'O elemento demorou muito para carregar!'
        except NoSuchElementException:
            return f'O elemento não foi encontrado!'
    
    #Abrir formulario de registro------------------------------
    def abrir_formulario(self, data):
        try:
            waitDriver = wdWait(self.driver, 10)
            
            waitDriver.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'ant-btn-primary')
            )).click()
            
            waitDriver.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'ant-menu-item')
            )).click()
            
            waitDriver.until(EC.presence_of_element_located(
                (By.XPATH, "//span[@class='name-process' and text()='Solicitação de Mudança de Endereço V3']")
            )).click()
            
            self.preencher_form(data)
        except TimeoutException:
            return f'Erro: o elemento demorou para carregar!'
        except NoSuchElementException: 
            return f'Erro: Elemento não encontrado!'
    
    #Preencher formulario------------------------------
    def preencher_form(self, data):
        self.waitDriver = wdWait(self.driver, 10)
        
        time.sleep(3)
        self.waitDriver.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '.navbar.minimalist')
        )).click()
        
        #Acessa o IFRAME do formulario------------------------------
        self.waitDriver.until(EC.frame_to_be_available_and_switch_to_it(
            (By.ID, 'iframe-form-app')
        ))
        
        """
            Mapeamento do sitepara campos que aceitam preenchimento
        """
        map_site_preencher = [
            'NOME_CLIENTE',
            'CONTRATO',
            'CPF',
            'TELEFONE',
            'ENDERECO',
            'NUMERO',
            'COMPLEMENTO',
            'CEP',
            'BAIRRO',
            'CIDADE',
            'ENDERECO_DESTINO',
            'NUMERO_DESTINO',
            'COMPLEMENTO_DESTINO',
            'CEP_DESTINO',
            'BAIRRO_DESTINO',
            'DATA_MUDANCA',
        ]
        
        """
            Mapeamento do site para os campos que precisam ser
            de um seleção de opção!
        """
        map_site_selecionar = [
            'TIPO_CLIENTE2',
            'CIDADE_ATENDIDA',
            'CANAL_ATENDIMENTO',
            'EQUIPE_OPE',
            'NIVEL_PRIORIDADE',
            'ESTADO_CLIENTE',
            'MESMA_CIDADE',
            'PREDIO',
            'COBERTURA',
            'OS_CAMPO',
        ]
        
        #dados do formulario------------------------------
        dados_RPA = data
        dados_RPA['DATA_MUDANCA'] = date.today().strftime('%d%m%Y')
        
        #preenche os campos que não precisa de seleção------------------------------
        """
            Faz um for no mapa do site(map_site_preencher) e verifica
            os dados para preencher
        """
        for dado in map_site_preencher:
            try:
                if dado == False or dado == '':
                    continue
                else:
                    self.waitDriver.until(EC.presence_of_element_located(
                        (By.XPATH, f"//input[@id='{dado}']")
                    )).send_keys(dados_RPA[dado])
            except NoSuchElementException:
                return f'Erro na busca do elemento'
            except TimeoutException:
                return f"Tempo limite excedido"
        
        #selecionar opções------------------------------
        """
            Faz um for em map_site_selecionar chamando a função
            para selecionar campo por campo
            Ele chama a função ao fina ldo codigo(input_select)
        """
        try:
            for data_select in map_site_selecionar:
                self.input_select(data_select, dados_RPA[data_select])
        except NoSuchElementException:
            return f"ERRO: Elemento não encontrado"
        except TimeoutException:
            return f"TIMEOUT: erro na seleção de"
            
        #preenche a cidade de destino------------------------------
        try:
            map_cid_dest = {
                'ES':'CIDADE_DESTINO_ES',
                'GO':'CIDADE_DESTINO_GO',
                'MG':'CIDADE_DESTINO_MG',
                'MS':'CIDADE_DESTINO_MS',
                'PR':'CIDADE_PARANA',
                'RJ':'CIDADES_RJ',
                'RS':'CIDADE_RS',
                'SC':'CIDADE_SC',
                'SP':'CIDADES_SP',
                'DF':'CIDADE_DF',
            }
            
            self.waitDriver.until(EC.presence_of_element_located(
                (By.ID, map_cid_dest[dados_RPA['ESTADO_CLIENTE']])
            )).click()
            
            self.waitDriver.until(EC.presence_of_element_located(
                (By.XPATH, f"//li[contains(@class, 'input-autocomplete__option')]//span[text()='{dados_RPA['CIDADE_CLIENTE']}']")
            )).click()
        except NoSuchElementException:
            return f"ERRO: cidade não encontrada!"
        except TimeoutError:
            return f"TIMEOUT: Erro no tempo de preenchimneto de cidade"
            
        #Prencher textarea OBS------------------------------
        try:
            self.waitDriver.until(EC.presence_of_element_located(
                (By.ID, 'OBS')
            )).send_keys(dados_RPA['OBS'])
        except NoSuchElementException:
            return f"Erro no preenchimneto de observação"
        except TimeoutException:
            return f"TIMEOUT: erro ao preencher OBS"
        
        #Preenche dados do predio------------------------------
        def data_pred_s():
            try:
                map_pred_site = [
                    'NOME_PREDIO',
                    'BLOCOS',
                    'QNT_ANDARES',
                    'NOME_SINDITO',
                    'TELEFONE_SINDICO',
                    'NOME_ZELADOR',
                    'TELEFONE_ZELADOR',
                ]
                
                for data in map_pred_site:
                    value = dados_RPA['INFO_PREDIO'][data]
                    self.waitDriver.until(EC.presence_of_element_located(
                        (By.ID, data)
                    )).send_keys(value)
            except NoSuchElementException:
                return f"Erro ao preencher dados de infomações sobre o predio/condominio"
            except TimeoutException:
                return f"TIMEOUT: erro no preenchimento de informaçoes sobre o predio/condominio"
        
        if dados_RPA['PREDIO'] == 's' or dados_RPA['PREDIO'] == 'sim':
            data_pred_s()
        
        #finalizar registro------------------------------
        try:
            self.waitDriver.until(EC.presence_of_element_located(
                (By.ID, 'aprovar')
            )).click()
            
            return f"Cadastro realizado!"
        except NoSuchElementException:
            return f"Erro ao finalizar registro"
        except TimeoutException:
            return f"TIMEOUT: erro na finalização do registro"

    #Função para selecionar opção------------------------------
    """
        Função para clicar e escrever em inputs que preecisam de uma seleção
        Clica na opção correspondente
    """
    def input_select(self, elemento, data):
        try:
            waitDriver = wdWait(self.driver, 10)
        
            waitDriver.until(EC.presence_of_element_located(
                (By.ID, elemento)
            )).click()
            
            waitDriver.until(EC.presence_of_element_located(
                (By.ID, f'{elemento}__search')
            )).send_keys(data)
            
            waitDriver.until(EC.presence_of_element_located(
                (By.ID, f'{elemento}_list')
            )).click()
        except TimeoutException:
            return f'TIMEOUT: Erro no preenchimento, tempo excedido -({elemento})-'
        except NoSuchElementException:
            return f'Elemento não encontrado: {elemento}'

@router.post('/api/rpa/mudanca_endereco')
async def executar_rpa(request: Request):
    bot = scraping()
    
    try:
        data = await request.json()
        
        bot.abrir_site(data)
        
        return JSONResponse(content={'Resultado': True, 'Mensagem': 'Cadastro reaalizado com sucesso!'},
        media_type='application/json')
    except Exception as e:
        return JSONResponse(content={'Resultado': False, 'Erro': str(e)},
        media_type='application/json')