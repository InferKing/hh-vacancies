from dash import html, Input, Output, State, callback, register_page, dcc, Patch
from dash_ag_grid import AgGrid
import dash_bootstrap_components as dbc
from api import HHParser


register_page(__name__, path='/', title="Главная")

tab1 = dbc.Container([
    dbc.Modal(id="modal_info", children=[
        dbc.ModalHeader(dbc.ModalTitle(id="modal_info_header")),
        dbc.ModalBody([
            AgGrid(id="modal_grid", className="ag-theme-alpine", dashGridOptions={'domLayout': 'autoHeight'}),
            html.Div([
                html.Div(id="modal_skills", className="my-2"),
                dcc.Markdown(id="modal_description", dangerously_allow_html=True),
            ], className="p-2 bg-light rounded")
        ]),
    ], is_open=False, size="xl", centered=True),
    dbc.Row([
        html.H1("Сборник вакансий с hh.ru", className="text-center pt-3"),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Input(id="search", type="text", placeholder="Название вакансии"),
            ]),
            dbc.Row([
                dbc.Switch(id="prefer_my_profile", label="Учитывать мой профиль", label_class_name="fs-6"),
            ], class_name="pt-2"),
        ], class_name="col-lg-6 col-sm-8 col-12"),
        dbc.Col([
            dbc.Button([
                html.I(className="bi bi-search me-2"),
                "Найти"
            ], id="search_button", color="primary", class_name="w-100"),
        ], class_name="col-lg-2 col-sm-4 col-12 p-0 ps-sm-2"),
    ], className="p-2 mb-3 justify-content-center"),
    dbc.Row([
        dcc.Loading(id="loading", children=AgGrid(
            id="grid", 
            className="ag-theme-alpine", 
            style={"display": "none"}, dashGridOptions={
                'pagination':True, 
                'paginationPageSize': 20, 
                'domLayout': 'autoHeight',
                },
            ), type="circle", fullscreen=True, color="red"),
    ])
], fluid=True)

tab2 = dbc.Container([
    dbc.Row(html.H2("Профиль", className="text-center p-3")),
    dbc.Row([
        html.Div("В разработке")
    ])
])


layout = dbc.Tabs([
    dbc.Tab(content, label=name, active_label_style={"letterSpacing": "0.1em", "textTransform": "uppercase"})
     for name, content in zip(["Вакансии", "Профиль"], [tab1, tab2])
], class_name="mt-2")



@callback(
    Output("grid", "rowData"),
    Output("grid", "columnDefs"),
    Output("grid", "style"),
    Input("search", "n_submit"),
    Input("search_button", "n_clicks"),
    State("search", "value"),
    State("prefer_my_profile", "value"),
    prevent_initial_call=True
)
def on_search(n_submit, n_clicks, search, prefer_my_profile):
    if n_submit or n_clicks:
        parser = HHParser()
        df = parser.make_request_all(text=search)

        return df.to_dict("records"), parser.grid_fields, {"display": "block"}


@callback(
    Output("modal_info", "is_open"),
    Output("modal_info_header", "children"),
    Output("modal_grid", "rowData"),
    Output("modal_grid", "columnDefs"),
    Output("modal_skills", "children"),
    Output("modal_description", "children"),
    Input("grid", "cellRendererData"),
    State("grid", "rowData"),
    prevent_initial_call=True
)
def on_more_info_clicked(render, data):
    from_grid = data[render["rowIndex"]]

    parser = HHParser()
    df = parser.make_request_by_id(from_grid["ID"])
    header = df["Название вакансии"].iloc[0]
    skills = df["Навыки"].iloc[0]
    description = df["Описание"].iloc[0]

    return True, header, df.to_dict("records"), parser.grid_fields_by_id, "Навыки: " + skills, description