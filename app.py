from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from config import DevelopmentConfig

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div([
    dcc.Store(id='store'),
    page_container
])

if __name__ == '__main__':
    app.run(**DevelopmentConfig().to_dict())