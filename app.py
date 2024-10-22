from dash import Dash, html, dcc, page_container
from dash_bootstrap_components import themes, icons
from utils.config import DevelopmentConfig, ProductionConfig

app = Dash(__name__, external_stylesheets=[themes.SIMPLEX, icons.BOOTSTRAP], use_pages=True)

app.layout = html.Div([
    dcc.Store(id='store'),
    page_container
])

if __name__ == '__main__':
    app.run(**ProductionConfig().to_dict())