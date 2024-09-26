from dash import register_page
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from model import Model

register_page(__name__, path='/profile', title="Профиль")

layout = dbc.Container([
    html.H1("Профиль"),
    html.Hr(),
    dbc.Breadcrumb(items=[
        {"href": "/", "label": "Главная"},
        {"label": "Профиль", "active": True},
    ]),
    dbc.Row([
        
    ])
])