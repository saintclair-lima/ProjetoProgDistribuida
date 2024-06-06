# Dados
## Origem e Formato

Os dados usados para este projeto foram obtidos a partir de Boletins informativos e casos do coronavírus por município por dia obtidos dos boletins das Secretarias Estaduais de Saúde. Estão disponíveis para download na página https://brasil.io/dataset/covid19/caso/

Estão organizados nas seguintes colunas:
* city
* city_ibge_cod
* date
* epidemiological_week
* estimated_population
* estimated_population_2019
* is_last
* is_repeated
* last_available_confirmed
* last_available_confirmed_per_100k_inhabitants
* last_available_date
* last_available_death_rate
* last_available_deaths
* order_for_place
* place_type
* state
* new_confirmed
* new_deaths
  
O conjunto de dados conta com 3.853.648 entradas, cada uma correspondendo a um conjunto de dados diários sobre COVID em um determinado município/unidade federativa brasleira.

De forma a simplificar o processo de análise, os dados foram ordenados por data de geração e foi adicionada uma coluna (num_item), a qual servirá de id de cada entrada.

Ademais, visto que os dados no conjunto possuem um caráter cronológico, os dados foram ordenados por data de referência das informações (coluna `date`).

Os dados modificados estão acessíveis para download em formato cvs (https://drive.google.com/file/d/1fPgwazLOF9MnHmcXMJrgWKlyhNwwu9Rf/view?usp=sharing) bem como diretamente como um arquivo sqlite3 (https://drive.google.com/file/d/1nOxbOQB9cY8Odp1_st6a4klDCi-dLyKl/view?usp=sharing).

## Modificação nos Dados
O objetivo dos dados é serem processados para serem enviados a um Context Broker (Orion) em uma estrutura Fiware, emulando um fluxo contínuo de dados sendo gerados e publicados dia a dia, pelas Secretarias de Saúde de Municípios e Estados brasileiros. Para simplificar o processo, os dados foram migrados do arquivo CSV original para um banco de dados SQLite, como formato intermediário ao formato alvo final.

De forma a ser aceito pelo Orion, os dados necessariamente devem estar de acordo com as especificações do NGSI (as quais são brevemente introduzidas nesta página https://fiware-zone.readthedocs.io/es/stable/getting-started.html). Dessa forma, as colunas acima são formatadas no seguinte modelo de dados:
```json
{
  "type": "Daily_COVID_Cases_In_City",
  "id": "urn:ngsi-ld:Daily_COVID_Cases_In_City:2",
  "cidade": {
    "type": "Text",
    "value": ""
  },
  "codigo_cidade_IBGE": {
    "type": "Text",
    "value": 12
  },
  "data": {
    "type": "Date",
    "value": "2020-03-17"
  },
  "semana_epidemiologica": {
    "type": "Integer",
    "value": 202012
  },
  "populacao_estimada": {
    "type": "Numeric",
    "value": 894470
  },
  "populacao_estimada_2019": {
    "type": "Numeric",
    "value": 881935
  },
  "ultima": {
    "type": "Boolean",
    "value": "false"
  },
  "repetida": {
    "type": "Boolean",
    "value": "false"
  },
  "ultimo_confirmados_disponivel": {
    "type": "Numeric",
    "value": 3
  },
  "ultimo_confirmados_por_100K_habit_disponivel": {
    "type": "Numeric",
    "value": 0.33539
  },
  "ultimo_data_disponivel": {
    "type": "Date",
    "value": "2020-03-17"
  },
  "ultimo_taxa_de_obito_disponivel": {
    "type": "Numeric",
    "value": 0
  },
  "ultimo_obitos_disponivel": {
    "type": "Numeric",
    "value": 0
  },
  "ordem_da_localidade": {
    "type": "Numeric",
    "value": 1
  },
  "tipo_da_localidade": {
    "type": "Text",
    "value": "state"
  },
  "unidade_federativa": {
    "type": "Text",
    "value": "AC"
  },
  "novo_confirmados": {
    "type": "Numeric",
    "value": 3
  },
  "novo_obitos": {
    "type": "Numeric",
    "value": 0
  }
}
```
# Informações sobre os municípios
De forma a possibilitar a distrbuição dos dados por município em alguma representação gráfica, foram adicionadas informações do IBGE reference aos municípios.
OS dados foram coletado da página do IBGE para publicação (https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/localidades/) e processadas, resultando no arquivo csv `municipios.csv` ou em sqlite, no arquivo `municipios.db`.

Dada a distância temporal entre os dois datasets, há 6 municípios que constam do dataset de casos de COVID, porém não estavam na publicação do IBGE. Esses municípios têm pouco mais de 3.000 instâncias de relatório de casos diários de COVID no dataset de casos de covid.

A entidade de modelagem de municípios no Orion está no seguinte formato:
```json
{
    "type" : "GeoLocationBrazilianMunicipality",
    "id" : "urn:ngsi-ld:GeoLocationBrazilianMunicipality:{registro[0]}",
    "municipality" : {
    "type" : "Text",
    "value" : "Taperoá"
    },
    "state" : {
    "type" : "Text",
    "value" : "PB"
    },
    "category" : {
    "type" : "Text",
    "value" : "city"
    },
    "longitude" : {
    "type" : "Numeric",
    "value" : -3.321654
    },
    "latitude" : {
    "type" : "Numeric",
    "value" : -32.321654
    },
    "altitude" : {
    "type" : "Numeric",
    "value" : 125.0
    }
}
```
