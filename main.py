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


df = pd.read_csv("./dataset/HIST_PAINEL_COVIDBR_13mai2021.csv", sep=";")

# "~" representa o operador binário NOT 
# ref.: https://pt.stackoverflow.com/questions/543283/uso-do-acento-til-no-python
df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]

df_brasil = df[df["regiao"] == "Brasil"]

# exportando como csv
df_brasil.to_csv("df_brasil.csv")
df_brasil.to_csv("df_states.csv")



