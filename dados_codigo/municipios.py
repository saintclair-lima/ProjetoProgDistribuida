import sqlite3
import json
import requests

def formatar_registro(registro, verboso=False):
  reg_formatado = {
    "type" : "GeoLocationBrazilianMunicipality",
    "id" : f"urn:ngsi-ld:GeoLocationBrazilianMunicipality:{registro[0]}",
    "municipality" : {
    "type" : "Text",
    "value" : registro[1]
    },
    "state" : {
    "type" : "Text",
    "value" : registro[2]
    },
    "category" : {
    "type" : "Text",
    "value" : registro[3]
    },
    "longitude" : {
    "type" : "Numeric",
    "value" : registro[4]
    },
    "latitude" : {
    "type" : "Numeric",
    "value" : registro[5]
    },
    "altitude" : {
    "type" : "Numeric",
    "value" : registro[6]
    },
  }
  if verboso:
    print('Registro formatado:')
    print(reg_formatado, '\n')
  return reg_formatado

conexao = sqlite3.connect('municipios.db')
cursor = conexao.cursor()

resultado = cursor.execute('SELECT * FROM municipios')
valores = resultado.fetchall()
conexao.commit()
conexao.close()

vals_formatados = [formatar_registro(item) for item in valores]
with open('log_municipios.txt', 'w') as arq:  
  for idx in range(len(vals_formatados)):
    msg = f'>>> Enviando item {idx} de {len(vals_formatados)}...'
    arq.write(msg + '\n')
    print(msg)
    item = vals_formatados[idx]
    payload = json.dumps(item, ensure_ascii=False)
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://10.3.225.203:1026/v2/entities', headers=headers, data=payload)
    msg = f'>>> Status do Envio {response.status_code} - {response.reason}\n'
    arq.write(msg + '\n')
    print(msg)