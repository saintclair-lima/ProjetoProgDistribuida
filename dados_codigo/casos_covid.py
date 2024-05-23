import sqlite3
import json
import requests
import time

URL_ORION = 'http://localhost:1026/v2/entities'

class Tabela:
  def __init__(self, banco_de_dados, tabela):
    self.banco_de_dados = banco_de_dados
    self.tabela = tabela
    self.conexao = sqlite3.connect(tabela)
    self.cursor = self.conexao.cursor()

  def selectColunaValor(self, coluna, valor):
    resultado = self.cursor.execute(f'SELECT * FROM {self.tabela} WHERE {coluna} = {valor}')
    return resultado.fetchall()

  def selectFlexivel(self, condicao_where=''):
    query = f'SELECT * FROM {self.tabela} ' + condicao_where
    print(f'Query resultante:\n{query}')
    resultado = self.cursor.execute(query)
    return resultado.fetchall()

class NGSI_Wrapper:
  def __init__(self, banco_de_dados, tabela, offset=0):
    self.offset = offset
    self.tabela = Tabela(banco_de_dados, tabela)
  
  def selectProximo(self):
    query = f'LIMIT 1 OFFSET {self.offset}'
    resultado = self.tabela.selectFlexivel(query)
    self.offset += 1
    return resultado
  
  def get_proximo_valor_formatado(self, verboso=False):
    linha_tabela = self.selectProximo()[0]
    payload = {
        "type" : "Daily_COVID_Cases_In_City",
        "id" : f"urn:ngsi-ld:Daily_COVID_Cases_In_City:{linha_tabela[0]}",
        "cidade" : {
            "type" : "Text",
            "value" : linha_tabela[1]
        },
        "codigo_cidade_IBGE" : {
            "type" : "Text",
            "value" : linha_tabela[2]
        },
        "data" : {
            "type" : "Date",
            "value" : linha_tabela[3]
        },
        "semana_epidemiologica" : {
            "type" : "Integer",
            "value" : linha_tabela[4]
        },
        "populacao_estimada" : {
            "type" : "Numeric",
            "value" : linha_tabela[5]
        },
        "populacao_estimada_2019" : {
            "type" : "Numeric",
            "value" : linha_tabela[6]
        },
        "ultima" : {
            "type" : "Boolean",
            "value" : str(linha_tabela[7]==1).lower()
        },
        "repetida" : {
            "type" : "Boolean",
            "value" : str(linha_tabela[8]==1).lower()
        },
        "ultimo_confirmados_disponivel" : {
            "type" : "Numeric",
            "value" : linha_tabela[9]
        },
        "ultimo_confirmados_por_100K_habit_disponivel" : {
            "type" : "Numeric",
            "value" : linha_tabela[10]
        },
        "ultimo_data_disponivel" : {
            "type" : "Date",
            "value" : linha_tabela[11]
        },
        "ultimo_taxa_de_obito_disponivel" : {
            "type" : "Numeric",
            "value" : linha_tabela[12]
        },
        "ultimo_obitos_disponivel" : {
            "type" : "Numeric",
            "value" : linha_tabela[13]
        },
        "ordem_da_localidade" : {
            "type" : "Numeric",
            "value" : linha_tabela[14]
        },
        "tipo_da_localidade" : {
            "type" : "Text",
            "value" : linha_tabela[15]
        },
        "unidade_federativa" : {
            "type" : "Text",
            "value" : linha_tabela[16]
        },
        "novo_confirmados" : {
            "type" : "Numeric",
            "value" : linha_tabela[17]
        },
        "novo_obitos" : {
            "type" : "Numeric",
            "value" : linha_tabela[18]
        },
    }

    obj_json = json.dumps(payload, ensure_ascii=False)
    if verboso: print(obj_json)
    return obj_json

  def post_proximo_valor(self, verboso=False):
    payload = self.get_proximo_valor_formatado(verboso=verboso)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL_ORION, headers=headers, data=payload)
    print(response.status_code)
    print(response.reason)
    print(response.text)

  def gerar_fluxo_dados(self, verboso=False, intervalo=5):
    contador = 0
    while contador < 200:
        self.post_proximo_valor(verboso=verboso)
        time.sleep(intervalo)

    response = requests.get('http://localhost:1026/v2/entities?type=Daily_COVID_Cases_In_City&options=keyValues')
    print(response.status_code)
    print(response.reason)
    print(response.text)

    print('CONCLUÍDO')


poster = NGSI_Wrapper('casos_covid', 'casos_covid', 8)
poster.gerar_fluxo_dados(verboso=False)
