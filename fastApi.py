from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import time

router = APIRouter()

class MudendAdapter():
    def __init__(self):
        # Configurar as opções do Chrome
        chrome_options = Options()
        #chrome_options.add_argument("--headless=old")  # Ativa o modo headless
        #chrome_options.add_argument("--disable-gpu")  # Necessário em algumas versões
        #chrome_options.add_argument("--no-sandbox")
        #chrome_options.add_argument("--disable-dev-shm-usage")  # Para contornar problemas em sistemas Linux

        # Inicia o navegador no modo headless
        self.servico = Service(ChromeDriverManager().install())
        self.adapter = webdriver.Chrome(service=self.servico, options=chrome_options)
        #self.adapter.maximize_window()


# FAZ O ACESSO À PÁGINA
    def acessar_pagina(self):
        try:
            self.adapter.get("https://adapter.veronet.com.br/adapter/#/login")
            time.sleep(5)
            print("Página acessada.")
        except Exception as e:
            print(f"Erro ao acessar a página {e}")

# FAZ O LOGIN NA PÁGINA
    def fazer_login(self):
        try:
            time.sleep(3)
            campo1 = WebDriverWait(self.adapter, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]')))
            campo1.send_keys("servico_thato")
            campo2 = WebDriverWait(self.adapter, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="senha"]')))
            campo2.send_keys("3tahto@t@hT0")
            botao1 = WebDriverWait(self.adapter, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="body"]/div[1]/section/div/form/div/button')))
            botao1.click()
            print("Login feito com sucesso!")
            time.sleep(5)
        except Exception as e:
            print(f"Erro ao fazer o login {e}")

    def navegar(self, cpf, protocolo):
        try:
            time.sleep(2)
            botaoComercial = self.adapter.find_element('xpath', '//*[@id="side-nav"]/li[5]/a')
            botaoComercial.click()
            time.sleep(2)
            botaoCliente = self.adapter.find_element('xpath', '//*[@id="36-collapse"]/li[1]/a')
            botaoCliente.click()
            campoCPF = self.adapter.find_element('xpath', '//*[@id="content-container"]/div/div/section/div/form/fieldset/div[2]/div[2]/input')
            campoCPF.send_keys(cpf)
            botaoPesquisar = WebDriverWait(self.adapter, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                               '//*[@id="content-container"]/div/div/section/div/form/fieldset/div[10]/button')))
            botaoPesquisar.click()
            botaoEditar =  WebDriverWait(self.adapter, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                   '/html/body/div[2]/div[2]/div/div[2]/div/section/div/div/div/table/tbody/tr/td[4]/div/a/span')))
            botaoEditar.click()
            time.sleep(2)
            # tratar alertas(fechar janelas)
            while True:
                try:
                    # Localiza o botão "OK" no popup
                    botao_ok = WebDriverWait(self.adapter, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//button[text()="OK"]'))
                    )
                    # Clica no botão "OK" usando JavaScript para evitar problemas de interceptação
                    self.adapter.execute_script("arguments[0].click();", botao_ok)
                    print("Popup fechado.")
                    time.sleep(1)  # Aguarda um segundo para o próximo popup aparecer, se houver
                except TimeoutException:
                    # Sai do loop se o botão "OK" não estiver presente
                    break
            time.sleep(7)
            abaAtendimentos = WebDriverWait(self.adapter, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                   '//*[@id="content-container"]/div[1]/ul/li[6]/a')))
            abaAtendimentos.click()
            #Maximizar a tela
            self.adapter.maximize_window()
            botaoExibir = WebDriverWait(self.adapter, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                   '//*[@id="content-container"]/div[2]/div/section/div/div[1]/div[1]/div/legend/div/div/div[2]/a/strong')))
            botaoExibir.click()
            campoProtocolo = self.adapter.find_element('xpath',
                                             '//*[@id="numeroProtocolo"]')
            campoProtocolo.send_keys(protocolo)
            botaoPesqAtend = WebDriverWait(self.adapter, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                   '//*[@id="content-container"]/div[2]/div/section/div/div[1]/div[1]/div/div/form/fieldset/div[9]/div/button[1]')))
            botaoPesqAtend.click()
            botaoEditar2 = WebDriverWait(self.adapter, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                   '/html/body/div[2]/div[2]/div/div[2]/div/section/div/div[1]/div[2]/div/section/div/div/div/div[2]/div[2]/table/tbody/tr/td[11]/div/a')))
            botaoEditar2.click()

        except Exception as e:
            print(f"Erro ao encontrar atendimento {e}")

    def preencher(self, descricao):
        time.sleep(2)
        try:
            campoDescricao = WebDriverWait(self.adapter, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                   '//*[@id="descricao"]')))
            campoDescricao.send_keys(descricao)
            #time.sleep(2)
            botaoSalvar = WebDriverWait(self.adapter, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                   '//*[@id="content-container"]/div[2]/div/section/div/div[1]/div/div/div/form/fieldset/div[13]/div/button[2]')))
            self.adapter.execute_script("arguments[0].scrollIntoView();", botaoSalvar)
            botaoSalvar.click()

            resultado = "Endereço modificado com sucesso!"

            print("Endereço modificado com sucesso!")

            return resultado

        except Exception as e:
            resultado = f"Erro ao modificar o endereço {e}"

            print(f"Erro ao modificar o endereço {e}")

#Código da API Fastapi
@router.post("/api/adapter_mudend")
async def post_consultar(
    cpf: str,
    protocolo: str,
    descricao: str,
    authorization: Optional[str] = Header(None)
):
    if authorization != '9uwPfXBjm04RNbWqZ1dU4vFkXJh3xhPSf5o78wC8':
        raise HTTPException(status_code=401, detail="Não autorizado.")

    try:
        adapter = MudendAdapter()
        adapter.acessar_pagina()
        adapter.fazer_login()
        adapter.navegar(cpf, protocolo)
        resultado = adapter.preencher(descricao) 
        return JSONResponse(content={"resultado": resultado}, media_type="application/json")


    except Exception as e:
        return JSONResponse(content={"resultado": False, "error": str(e)}, media_type="application/json")