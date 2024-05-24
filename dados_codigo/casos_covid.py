import sqlite3
import json
import requests
import time

URL_ORION = 'http://localhost:1026/v2/entities'

class Tabela:
  def __init__(self, banco_de_dados, tabela):
    self.banco_de_dados = banco_de_dados
    self.tabela = tabela
    self.conexao = sqlite3.connect(self.banco_de_dados)
    self.cursor = self.conexao.cursor()

  def executar(self, query):
    resultado = self.cursor.execute(query)
    valores = resultado.fetchall()
    self.conexao.commit()
    return valores

  def encerrar_conexao(self):
    self.conexao.close()

class NGSI_Wrapper:
  def __init__(self, banco_de_dados, tabela):
    self.tabela = Tabela(banco_de_dados, tabela)

  def encerrar_conexao(self):
    self.tabela.encerrar_conexao()
  
  def executar_query(self, query):
    resultado = self.tabela.executar(query)
    return resultado

  def get_registro_formatado(self, registro, verboso=False):
    reg_formatado = {
      "type" : "Daily_COVID_Cases_In_City",
      "id" : f"urn:ngsi-ld:Daily_COVID_Cases_In_City:{registro[0]}",
      "cidade" : {
        "type" : "Text",
        "value" : registro[1]
      },
      "codigo_cidade_IBGE" : {
        "type" : "Text",
        "value" : registro[2]
      },
      "data" : {
        "type" : "Date",
        "value" : registro[3]
      },
      "semana_epidemiologica" : {
        "type" : "Integer",
        "value" : registro[4]
      },
      "populacao_estimada" : {
        "type" : "Numeric",
        "value" : registro[5]
      },
      "populacao_estimada_2019" : {
        "type" : "Numeric",
        "value" : registro[6]
      },
      "ultima" : {
        "type" : "Boolean",
        "value" : str(registro[7]==1).lower()
      },
      "repetida" : {
        "type" : "Boolean",
        "value" : str(registro[8]==1).lower()
      },
      "ultimo_confirmados_disponivel" : {
        "type" : "Numeric",
        "value" : registro[9]
      },
      "ultimo_confirmados_por_100K_habit_disponivel" : {
        "type" : "Numeric",
        "value" : registro[10]
      },
      "ultimo_data_disponivel" : {
        "type" : "Date",
        "value" : registro[11]
      },
      "ultimo_taxa_de_obito_disponivel" : {
        "type" : "Numeric",
        "value" : registro[12]
      },
      "ultimo_obitos_disponivel" : {
        "type" : "Numeric",
        "value" : registro[13]
      },
      "ordem_da_localidade" : {
        "type" : "Numeric",
        "value" : registro[14]
      },
      "tipo_da_localidade" : {
        "type" : "Text",
        "value" : registro[15]
      },
      "unidade_federativa" : {
        "type" : "Text",
        "value" : registro[16]
      },
      "novo_confirmados" : {
        "type" : "Numeric",
        "value" : registro[17]
      },
      "novo_obitos" : {
        "type" : "Numeric",
        "value" : registro[18]
      },
    }
    
    if verboso:
      print('Registro formatado:')
      print(reg_formatado, '\n')
    return reg_formatado

  def enviar_proximo_batch(self, verboso=False):
    # selecionando próximo lote de envio
    query = 'select * from casos_covid where date in (select date from casos_covid where sent_to_broker <> 1 order by date limit(1)) and sent_to_broker=0;'
    prox_lote = self.executar_query(query)
    qtd_itens = len(prox_lote)
    intervalo = 60 / (len(prox_lote))
    if intervalo > 10: intervalo = 5
    if intervalo < 1: intervalo = 1
    
    if verboso: print(f"Enviando {qtd_itens} entradas ao broker (1 a cada {intervalo} segs.)")
    for idx in range(len(prox_lote)):
      item = prox_lote[idx]
      if verboso: print(f">>> Item com id {item[0]} - {idx + 1} de {qtd_itens}")
      reg_formatado = self.get_registro_formatado(item)
      payload = json.dumps(reg_formatado, ensure_ascii=False)
      headers = {'Content-Type': 'application/json'}
      response = requests.post(URL_ORION, headers=headers, data=payload)
      if response.status_code == 201:
        query = f'update casos_covid set sent_to_broker = 1 where num_item = {item[0]}'
        self.executar_query(query)
      if verboso:
        print(f'>>> Status do Envio {response.status_code}\n')
        if response.status_code != 201: print(response.reason)
      time.sleep(intervalo)

  def enviar_fluxo_ao_broker(self, verboso=True):
    num_registros_por_enviar = self.executar_query('select count(*) from casos_covid where sent_to_broker = 0')[0][0]
    while num_registros_por_enviar > 0:
      if verboso: print('ENVIANDO NOVO LOTE...')
      self.enviar_proximo_batch(verboso)
      if verboso: print('ENVIO DO LOTE FINALIZADO...\n\n')
    print('ENVIO DOS LOTES CONCLUÍDO')

  def gerar_fluxo_dados_sequencia(self, verboso=False, intervalo=5):
    contador = 0
    while contador < 200:
      self.post_proximo_valor(verboso=verboso)
      time.sleep(intervalo)

    response = requests.get('http://localhost:1026/v2/entities?type=Daily_COVID_Cases_In_City&options=keyValues')
    print(response.status_code)
    print(response.reason)
    print(response.text)
    print('CONCLUÍDO')


poster = NGSI_Wrapper('casos_covid.db', 'casos_covid')
poster.enviar_fluxo_ao_broker(verboso=True)
