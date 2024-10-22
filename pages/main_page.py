from dash import html, Input, Output, State, callback, register_page, dcc, Patch
from dash_ag_grid import AgGrid
import dash_bootstrap_components as dbc
from api import HHParser
from utils.enums import Currency, Experience, EnumReflector


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
        html.H1("Поиск вакансий с hh.ru", className="text-center pt-3"),
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
                'pagination': True, 
                'paginationPageSize': 20, 
                'domLayout': 'autoHeight',
                },
            ), type="circle", fullscreen=True, color="red"),
    ])
], fluid=True)

tab2 = dbc.Container([
    dbc.Row(html.H2("Профиль", className="text-center p-3")),
    dbc.Row([
        dbc.Row([
            dbc.Label("Город", html_for="city", class_name="fs-5"),
            dbc.Input(id="city", type="text", placeholder="Город")
        ], class_name="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Валюта", html_for="currency", class_name="fs-5"),
                dbc.Checklist([item for item in EnumReflector.reflect(Currency)], id="currency")
            ]),
            dbc.Col([
                dbc.Label("Опыт работы", html_for="experience", class_name="fs-5"),
                dbc.Checklist([item for item in EnumReflector.reflect(Experience)], id="experience")  
            ])
        ], class_name="mb-3"),
        dbc.Row([
            dbc.Col([
                dbc.Label("Зарплата От", html_for="pay_from", class_name="fs-5"),
                dbc.Input(id="pay_from", type="number", placeholder="Зарплата От")
            ]),
            dbc.Col([
                dbc.Label("Зарплата До", html_for="pay_to", class_name="fs-5"),
                dbc.Input(id="pay_to", type="number", placeholder="Зарплата До")
            ]),
        ], class_name="mb-3"),
        dbc.Row(
            dbc.Col(
                dbc.Button([
                    html.I(className="bi bi-save me-2"),
                    "Применить"  
                ], class_name="d-block w-100", color="primary", id="save_button"),
                class_name="col-lg-3 col-sm-6 col-12",
            )
        ), 
    ], className="p-3 mt-2 justify-content-center"),
])


layout = dbc.Tabs([
    dbc.Tab(content, label=name, active_label_style={"letterSpacing": "0.08em", "textTransform": "uppercase"})
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


@callback(
    Output("store", "data"),
    Input("save_button", "n_clicks"),
    State("city", "value"),
    State("currency", "value"),
    State("experience", "value"),
    State("pay_from", "value"),
    State("pay_to", "value"),
    prevent_initial_call=True
)
def on_save(n_clicks, city, currency, experience, pay_from, pay_to):
    # TODO: add save/load to storage
    # TODO: set filters to grid
    return {
        "city": city,
        "currency": currency,
        "experience": experience,
        "pay_from": pay_from,
        "pay_to": pay_to
    }