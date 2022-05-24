# iniciando o projeto
import dash # gerenciar o dashboard (criar servidor e manter layout)
import dash_core_components as dcc # criar componentes, seleção de data, dropdown, etc...
import dash_html_components as html # habilitar html no código
from dash.dependencies import Input, Output # interatividade
import dash_bootstrap_components as dbc

import plotly.express as px # express permite criar graficos de forma mais simples
import plotly.graph_objects as go # mais controle sobre graficos

import numpy as np
import pandas as pd
import json

# -- inicio do bloco comentado
  # df = pd.read_csv("./dataset/HIST_PAINEL_COVIDBR_13mai2021.csv", sep=";")

  # # "~" representa o operador binário NOT 
  # # ref.: https://pt.stackoverflow.com/questions/543283/uso-do-acento-til-no-python
  # df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]

  # df_brasil = df[df["regiao"] == "Brasil"]

  # # exportando como csv
  # df_brasil.to_csv("./dataset/df_brasil.csv")
  # df_brasil.to_csv("./dataset/df_states.csv")
# -- fim do bloco comentado

# importando novos datasets csv
df_states = pd.read_csv("./dataset/df_states.csv")
df_brasil = pd.read_csv("./dataset/df_brasil.csv")

# geojson
brasil_states = json.load(open("./geojson/brazil_geo.json", "r"))

# -- inicio do bloco comentado
  # type(brasil_states)
  # brasil_states.keys() # verificando as chaves do dict
  # type(brasil_states["features"]) # verificando o tipo da chave features
  # type(brasil_states["features"][0]) # verificando o tipo do primeiro elemento da lista
  # brasil_states["features"][0].keys() # verificando as chaves do primeiro elemento da lista que é um dict
# -- fim do bloco comentado






