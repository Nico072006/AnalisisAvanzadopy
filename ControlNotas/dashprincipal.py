import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, Input, Output, dash_table
from database import obtenerestudiantes

def creartablero(server):
    # Carga inicial de datos
    df = obtenerestudiantes()

    appnotas = dash.Dash(__name__, server=server,
                         url_base_pathname="/dashprincipal/",
                         suppress_callback_exceptions=True)

    appnotas.layout = html.Div([
        html.H1("TABLERO DE CONTROL ACADÉMICO", style={
            "textAlign": "center",
            "backgroundColor": "black",
            "color": "#FFFFFF",
            "padding": "30px",
            "borderRadius": "50px"
        }),

        # Filtros
        html.Div([
            html.Div([
                html.Label("Seleccionar carrera"),
                dcc.Dropdown(
                    id="filtro carrera",
                    options=[{"label": ca, "value": ca} for ca in sorted(df["Carrera"].unique())],
                    value=df["Carrera"].unique()[0]
                ),
            ], style={"width": "40%",
                    "display": "inline-block",
                    "padding": "20px",
                    "margin": "10px",
                    "color":"black",


                    }),

            html.Div([
                html.Label("Rango de Edad"),
                dcc.RangeSlider(
                    id="slider_EdadEstu",
                    min=df["EdadEstu"].min(),
                    max=df["EdadEstu"].max(),
                    step=1,
                    value=[df["EdadEstu"].min(), df["EdadEstu"].max()],
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={"width": "40%",
                    "display": "inline-block",
                    "padding": "20px"
                    }),

            html.Div([
                html.Label("Rango promedio"),
                dcc.RangeSlider(
                    id="slider_promedio",
                    min=0, max=5, step=0.1,
                    value=[0, 5],
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={"width": "40%",
                    "display": "inline-block", 
                    "padding": "20px"
                    }),

        ], style={"display": "flex",
                   "justifyContent": "center"
                   }),

        html.Br(),
        dcc.Input(id="busqueda", type="text", placeholder="Buscar por nombre...", 
                  style={"width": "50%",
                        "margin": "auto",
                        "display": "block", 
                        "padding": "10px",
                        "border": "1px solid black",
                        "border-radius": "50px",
                        }),
        
        html.Br(),
        dcc.Graph(id="gran_detallado"), 

        # KPIs
        html.Div(id="Kpis", style={"display": "flex", 
                                "justifyContent": "space-around", 
                                "margin": "30px"
                                }),

        # Tabla
        dcc.Loading(
            dash_table.DataTable(
                id="tabla",
                columns=[{"name": i, "id": i} for i in df.columns],
                page_size=8,
                filter_action="native",
                sort_action="native",
                row_selectable="multi",
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "center", "padding": "10px"},
                style_header={"backgroundColor": "#1a1a1a", "color": "#00f2ff", "fontWeight": "bold", "border": "1px solid #333"}
            ), type="circle"
        ),

        html.Br(),
        dcc.Loading(dcc.Graph(id="grafico_interactivo_tabla"), type="default"),

        # Tabs para gráficos adicionales
        dcc.Tabs([
            dcc.Tab(label="Distribución (Histograma)", children=[dcc.Graph(id="histograma")]),
            dcc.Tab(label="Dispersión Edad vs Promedio", children=[dcc.Graph(id="dispersion")]),
            dcc.Tab(label="Análisis por Edad", children=[dcc.Graph(id="pie")]),
            dcc.Tab(label="Rango de edad",children=[dcc.Graph(id="RangoEdad")])
        ]),

        dcc.Interval(id="intervalo", interval=30000, n_intervals=0) # 30 seg para refrescar
    ], style={"fontFamily": "Arial"})

    # Callback principal
    @appnotas.callback(
        Output("tabla", "data"),
        Output("tabla", "columns"),
        Output("Kpis", "children"),
        Output("gran_detallado", "figure"),
        Output("histograma", "figure"),
        Output("dispersion", "figure"),
        Output("pie", "figure"),
        Output("RangoEdad", "figure"),
        Input("filtro carrera", "value"),
        Input("slider_EdadEstu", "value"),
        Input("slider_promedio", "value"),
        Input("busqueda", "value"),
        Input("intervalo", "n_intervals")
    )
    def actualizar_comp(carrera, rangoEdad, rangoProme, busqueda, n):
        # Recargar datos de la BD en cada intervalo si es necesario
        dff = obtenerestudiantes()
        
        filtro = dff[
            (dff["Carrera"] == carrera) &
            (dff["EdadEstu"].between(rangoEdad[0], rangoEdad[1])) &
            (dff["Promedio"].between(rangoProme[0], rangoProme[1]))
        ]

        if busqueda:
            filtro = filtro[filtro["NombreEstu"].str.contains(busqueda, case=False, na=False)]

        # Cálculos de KPIs
        promedio_gral = round(filtro["Promedio"].mean(), 2) if not filtro.empty else 0
        total = len(filtro)
        maximo = round(filtro["Promedio"].max(), 2) if not filtro.empty else 0

        kpis = [
            html.Div([html.H4("Promedio Gral"), html.H2(promedio_gral)], className="kpi-card"),
            html.Div([html.H4("Estudiantes"), html.H2(total)], className="kpi-card"),
            html.Div([html.H4("Nota Máxima"), html.H2(maximo)], className="kpi-card"),
        ]




        # Nota: añade estilos CSS o clases para los kpi-card
        

        edadbar= px.bar(filtro.groupby("RangoEdad").size().reset_index(name="Cantidad"),
                        x="RangoEdad",
                        y="Cantidad",
                        title="Cantidad de Estudiantes por Edad")
        # Gráficos
        fig_barras = px.bar(filtro, x="NombreEstu", y="Promedio", title="Notas por Estudiante", color="Promedio")
        
        fig_hist = px.histogram(filtro, x="Promedio", title="Distribución de Notas", nbins=15)
        
        fig_disp = px.scatter(filtro, x="EdadEstu", y="Promedio", color="Carrera", size="Promedio",
                              hover_data=["NombreEstu"], title="Relación Edad vs Promedio")
        
        fig_pie = px.pie(filtro, names="Desempeno" if "Desempeno" in filtro.columns else "Desempeño", 
                         title="Distribución por Nivel de Desempeño")

        return (
            filtro.to_dict("records"),
            [{"name": i, "id": i} for i in filtro.columns],
            kpis, fig_barras, fig_hist, fig_disp, fig_pie
        )

    # Callback interactivo de la tabla
    @appnotas.callback(
        Output("grafico_interactivo_tabla", "figure"),
        Input("tabla", "derived_virtual_data"),
        Input("tabla", "derived_virtual_selected_rows")
    )
    def actualizartab(rows, selected_rows):
        if rows is None or len(rows) == 0:
            return px.scatter(title="Sin datos seleccionados")
        
        dff = pd.DataFrame(rows)
        if selected_rows:
            dff = dff.iloc[selected_rows]
        
        col_des = "Desempeno" if "Desempeno" in dff.columns else "Desempeño"
        
        fig = px.scatter(dff, x="EdadEstu", y="Promedio", color=col_des if col_des in dff.columns else None,
                         size="Promedio", title="Detalle de Estudiantes Seleccionados",
                         text="NombreEstu")
        return fig

    return appnotas