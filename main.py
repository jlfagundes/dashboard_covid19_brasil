# iniciando o projeto
from distutils.log import debug
import dash # gerenciar o dashboard (criar servidor e manter layout)
from dash import dcc # criar componentes, seleção de data, dropdown, etc...
from dash import html # habilitar html no código
from dash.dependencies import Input, Output # interatividade
import dash_bootstrap_components as dbc

import plotly.express as px # express permite criar graficos de forma mais simples
import plotly.graph_objs as go # mais controle sobre graficos

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

df_states_date = df_states[df_states["data"] == "2020-05-13"]

df_data = df_states[df_states["estado"] == "RJ"]

# geojson
brasil_states = json.load(open("./geojson/brazil_geo.json", "r"))

# -- inicio do bloco comentado
  # type(brasil_states)
  # brasil_states.keys() # verificando as chaves do dict
  # type(brasil_states["features"]) # verificando o tipo da chave features
  # type(brasil_states["features"][0]) # verificando o tipo do primeiro elemento da lista
  # brasil_states["features"][0].keys() # verificando as chaves do primeiro elemento da lista que é um dict
# -- fim do bloco comentado

# criando o mapa
# classe instânciando modulo Dash() que é o dashboard
# dbc.themes criando o tema do dashboar
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG]) 

# figure para armazenar o grafico do mapa
# mapas do tipo choropleth tem as divisões especificadas
# verificar colors na documentação do mapbox()
fig  = px.choropleth_mapbox(df_states_date, locations="estado", color="casosNovos", geojson=brasil_states, color_continuous_scale="Redor", opacity=0.4, hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": True}, center={"lat": -16.95, "lon": -47.78}, zoom=4)

# ref> https://plotly.com/python/reference/layout/
fig.update_layout(
  paper_bgcolor="#242424", # paleta de cores
  autosize=True,
  margin=go.layout.Margin(l=0, r=0, t=0, b=0),
  showlegend=False,
  mapbox_style="carto-darkmatter" # estilo escolher na documentação
)

# criarndo segundo gráfico de outra forma
fig2 = go.Figure(layout={"template": "plotly_dark"}) # criando uma Figure
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"])) # adicionando dataset, eixos x e y
fig2.update_layout(
  paper_bgcolor="#242424", # paleta de cores
  plot_bgcolor="#242424",
  margin=dict(l=10, r=10, t=10, b=10)

)


# criando o layout usando dbc layout

app.layout = dbc.Container (
  dbc.Row([
    dbc.Col([
      # componente do dash que guarda graficos
      dcc.Graph(id="line-graph", figure=fig2)
    ]),
    dbc.Col([
      dcc.Graph(id="choropleth-map", figure=fig)
    ])
  ])
)


if __name__ == "__main__":
  app.run_server(debug=True)
