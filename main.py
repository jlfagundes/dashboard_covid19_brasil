# iniciando o projeto
from distutils.log import debug
from gc import callbacks
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

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

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

select_columns = {
  "casosAcumulado": "Casos Acumulados",
  "casosNovos": "Casos Novos",
  "obitosAcumulado": "Óbitos Totais",
  "obitosNovos": "Óbitos por dia",
}

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
fig  = px.choropleth_mapbox(
  df_states_date,
  locations="estado",
  color="casosNovos",
  geojson=brasil_states,
  color_continuous_scale="Redor",
  opacity=0.4,
  hover_data={
    "casosAcumulado": True,
    "casosNovos": True,
    "obitosNovos": True,
    "estado": True
  },
  center={"lat": CENTER_LAT, "lon": CENTER_LON}, zoom=4)

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
  margin=dict(l=10, r=10, t=10, b=10),
  autosize=True
)


# criando o layout usando dbc layout

app.layout = dbc.Container (
  dbc.Row([
    dbc.Col([
      # usando tag HTML
      html.Div([
        html.Img(id="logo", alt="Logotipo da Empresa", src=app.get_asset_url("logo_cetti.png"), height=50),
        html.H5("Evolução COVID-19"),
        dbc.Button("BRASIL", color="primary", id="location-button", size="lg"),
      ], style={}), # customizando a div

      html.P("Informe a data na deseja obter informações:", style={"margin-top": "40px"}),

      html.Div(id="div-test", children=[
        # objeto que permite escolher uma data
        dcc.DatePickerSingle(
          id="date-picker",
          min_date_allowed=df_brasil["data"].min(),
          max_date_allowed=df_brasil["data"].max(),
          date=df_brasil["data"].min(),
          display_format="MMMM D, YYYY",
          style={"border": "0px solid black"}
        )
      ]),

      # criando os cards
      dbc.Row([
        dbc.Col([
          dbc.Card([
            dbc.CardBody([
              html.Span("Casos recuperados"),
              html.H3(style={"color": "#adfc92"}, id="casos-recuperados-text"),
              html.Span("Em acompanhamento"),
              html.H5(id="casos-em-acompanhamento-text"),
            ])
          ], color="light", outline=True, style={"margin-top": "10px",
            "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
            "color": "#FFFFFF"}) # color do boostrap dash
        ], md=4), # md largura da coluna 4 ocupa 1 terço do espaço
        dbc.Col([
          dbc.Card([
            dbc.CardBody([
              html.Span("Casos confirmados totais"),
              html.H3(style={"color": "#389fd6"}, id="casos-confirmados-text"),
              html.Span("Novos casos na data"),
              html.H5(id="novos-casos"),
            ])
          ], color="light", outline=True, style={"margin-top": "10px",
            "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
            "color": "#FFFFFF"}) 
        ], md=4),
        dbc.Col([
          dbc.Card([
            dbc.CardBody([
              html.Span("Obitos confirmados"),
              html.H3(style={"color": "#DF2935"}, id="obitos-confirmados-text"),
              html.Span("Obitos na data"),
              html.H5(id="obitos-data-text"),
            ])
          ], color="light", outline=True, style={"margin-top": "10px",
            "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
            "color": "#FFFFFF"}) 
        ], md=4),
      ]),

      html.Div([
        html.P("Selecione o tipo de dado que deseja visualizar", style={"margin-top": "25px"}),

        # Criando o dropDown
        dcc.Dropdown(id="location-dropdown",
          # laço for para percorrer array de colunas selecionadas, como opções
          options=[{"label": j, "value": i} for i, j in select_columns.items()],
          value="casosNovos",
          style={"margin-top": "10px"}
        ),

        # componente do dash que guarda graficos
        dcc.Graph(id="line-graph", figure=fig2)
      ])
    ], md=5, style={"padding": "25px", "background-color": "#242424"}),
    dbc.Col([
      # Criando loading para o map graph
      dcc.Loading(id="loading-1", type="default",
        children=[
          dcc.Graph(id="choropleth-map", figure=fig, style={"height": "100vh", "margin-right": "10px"})
        ]) # children = dentro do loading
    ], md=7)
  ])
, fluid=True) # fluid para largura total

# interatividade data and location

# usando decoradores do dash as funções abaixo sabem o que utilizar
@app.callback(
  # outputs da função
  [
    Output("casos-recuperados-text", "children"),
    Output("casos-em-acompanhamento-text", "children"),
    Output("casos-confirmados-text", "children"),
    Output("novos-casos", "children"),
    Output("obitos-confirmados-text", "children"),
    Output("obitos-data-text", "children"),
  ],
  # inputs da função (id, valor)
  [
    Input("date-picker", "date"),
    Input("location-button", "children")
  ]
)

def display_status(date, location):
  if location == "BRASIL":
    df_data_on_date = df_brasil[df_brasil["data"] == date]
  else:
    df_data_on_date = df_states[(df_states["estado"] == location) & (df_states["data"] == date)]

  # tratando o Nan dos recuperados novos
  # porque so tem do Brasil e não do estado
  recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".")
  acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0] else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".")
  casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0] else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".")
  casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0] else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".")
  obitos_acumulados = "-" if df_data_on_date["obitosAcumulado"].isna().values[0] else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".")
  obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0] else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".")


  # retorna todos os outputs
  return (
    recuperados_novos,
    acompanhamentos_novos,
    casos_acumulados,
    casos_novos,
    obitos_acumulados,
    obitos_novos,
  )


# interatividade graph dropdown
@app.callback(
  # se tem um output somente não passa lista []
  Output("line-graph", "figure"),
  # no input tem que ser lista []
  [
    Input("location-dropdown", "value"),
    Input("location-button", "children")
  ]
)

def plot_line_graph(plot_type, location):
  if location == "BRASIL":
    df_data_on_location = df_brasil.copy()
  else:
    df_data_on_location = df_states[df_states["estado"] == location]

  # colunas que vão ter graph type bar
  bar_plots = ["casosNovos", "obitosNovos"]

  fig2 = go.Figure(layout={"template": "plotly_dark"})
  if plot_type in bar_plots:
    fig2.add_trace(go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
  else:
    fig2.add_trace(go.Scatter(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))

  fig2.update_layout(
    paper_bgcolor="#242424", # paleta de cores
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
  )

  return fig2


# interatividade com o mapa
@app.callback(
  Output("choropleth-map", "figure"),
  [
    Input("date-picker", "date")
  ]
)

def update_map(date):
  df_data_on_states = df_states[df_states["data"] == date]

  fig = px.choropleth_mapbox(
    df_data_on_states,
    locations="estado",
    color="casosNovos",
    geojson=brasil_states,
    color_continuous_scale="Redor",
    opacity=0.4,
    hover_data={
      "casosAcumulado": True,
      "casosNovos": True,
      "obitosNovos": True,
      "estado": True
    },
    center={"lat": CENTER_LAT, "lon": CENTER_LON}, zoom=4
  )
  
  return fig


if __name__ == "__main__":
  app.run_server(debug=True)
