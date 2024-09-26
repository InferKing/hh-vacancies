from dash import register_page
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from model import Model

register_page(__name__, path='/', title="Главная")

layout = dbc.Container([
    html.H1("Главная страница"),
    html.Hr(),
    dbc.Row([
        
    ])
])