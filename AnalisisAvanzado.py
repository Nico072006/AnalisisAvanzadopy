import pandas as pd
import plotly.express as px
import os
import dash
from dash import html, dcc, Input, Output
from dash import dash_table
 
# cargar los datos
ruta = os.path.join(os.path.dirname(__file__), "notas_limpio.xlsx")
df = pd.read_excel(ruta)
 
# iniciar app
appnotas = dash.Dash(__name__)
 
appnotas.layout = html.Div([
    html.H1("TABLERO AVANZADO", style={
        "textAlign": "center",
        "backgroundColor": "#000000",
        "color": "#FFFFFF",
        "padding": "30px"
    }),
 
    # crear los filtros
    html.Div([
        html.Label("Seleccionar carrera"),
        dcc.Dropdown(
            id="filtro carrera",
            options=[{"label": ca, "value": ca} for ca in sorted(df["Carrera"].unique())],
            value=df["Carrera"].unique()[0]
        ),
        html.Br(),
 
        html.Label("Rango de edad"),
        dcc.RangeSlider(
            id="slider_edad",
            min=df["Edad"].min(),
            max=df["Edad"].max(),
            step=1,
            value=[df["Edad"].min(), df["Edad"].max()],
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        html.Br(),
 
        html.Label("Rango promedio"),
        dcc.RangeSlider(
            id="slider_promedio",
            min=0,
            max=5,
            step=0.1,
            value=[0, 5],
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ], style={"width": "80%", "margin": "auto"}),
 
    html.Br(),
 
    # crear los Kpis
    html.Div(id="Kpis",
             style={"display": "flex",
                    "justifyContent": "space-around"}),
    html.Br(),
 
    # crear una tabla
    dcc.Loading(
        dash_table.DataTable(
            id="tabla",
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=8,
            filter_action="native",
            sort_action="native",
            row_selectable="multi",
            selected_rows=[],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center"}
        ),
        type="circle"
    ),
    html.Br(),
 
    # crear el grafico interactivos
    dcc.Loading(
        dcc.Graph(id="grafico_interactivo_tabla"),
        type="default"
    ),
 
    html.Br(),
 
    # crear los tabs
    dcc.Tabs([
        dcc.Tab(label="Histograma", children=[dcc.Graph(id="histograma")]),
        dcc.Tab(label="Dispersion", children=[dcc.Graph(id="dispersion")]),
        dcc.Tab(label="Desempeño", children=[dcc.Graph(id="pie")]),
    ])                             
])
 
#actualizacion de la tabla y grafico general
 
@appnotas.callback(
    Output("tabla","data"),
    Output("tabla","columns"),
    Output("Kpis","children"),
    Output("gran_detallado","figure"),
    Output("histograma", "figure"),
    Output("dispersion", "figure"),
    Output("pie", "figure"),
    Input("filtro carrera","value"),
    Input("slider_edad", "value"),
    Input("slider_promedio", "value")

)
def actualizar_comp(carrera,rangoedad,rangoprome):
    filtro = df[
        (df["Carrera"]==carrera)&
        (df["Edad"]>=rangoedad[0])&
        (df["Edad"]<=rangoedad[1])&
        (df["Promedio"]>=rangoprome[0])&
        (df["Promedio"]<=rangoprome[1])
    ]
    promedio = round(filtro["Promedio"].mean(),2) if len(filtro) > 0 else 0
    total = len(filtro)
    maximo = round(filtro["Promedio"].max(),2) if len(filtro) > 0 else 0
    kpis= [
        html.Div([html.H4("Promedio"),html.H2(promedio)],
                 style={"backgroundColor":"#001aff",
                        "color":"white",
                        "padding":"30px",
                        "borderRadius":"50%",
                        "textAlign": "center"
                        }),
        html.Div([html.H4("Total Estudiantes"),html.H2(total)],
                 style={"backgroundColor":"#001aff",
                        "color":"white",
                        "padding":"30px",
                        "borderRadius":"50%",
                        "textAlign": "center"
                        }),
        html.Div([html.H4("Maximo"),html.H2(maximo)],
                 style={"backgroundColor":"#001aff",
                        "color":"white",
                        "padding":"30px",
                        "borderRadius":"50%",
                        "textAlign": "center"
                        }),
    ]

    df_barras= filtro.groupby("Carrera")["Promedio"].mean().reset_index()
    fig_barras = px.bar(df_barras, x="Carrera", y="Promedio", 
                        title="Desempeño Promedio por Carrera",
                        color="Promedio", color_continuous_scale="Viridis")

    fig_hist = px.histogram(filtro, x="Promedio", nbins=10,
                            title="Distribución de Frecuencia de Promedios",
                            color_discrete_sequence=['#1E1BD2'])
    
    fig_disp = px.scatter(filtro, x=filtro.index, y="Promedio", 
                          hover_name="Nombre" if "Nombre" in filtro.columns else None,
                          title="Dispersión Individual de Promedios",
                          color="Promedio")
                              

    fig_pie = px.pie(filtro, names="Edad", values="Promedio", 
                     title="Aporte de Promedio por Rango de Edad",
                     hole=0.3)
    
    return(
        filtro.to_dict("records"),
        [{"name":i,"id":i}for i in filtro.columns],
        kpis,
        fig_barras, 
        fig_hist,   
        fig_disp,   
        fig_pie    
    )

@appnotas.callback(
    Output("grafico_interactivo_tabla","figure"),
    Input("tabla","derived_virtual_data"),
    Input("tabla","derived_virtual_selected_rows")
)
def actualizartab(rows,selected_rows):
    if rows is None:
        return px.scatter(title="Sin Datos")
    dff =pd.DataFrame(rows)

    if selected_rows:
        dff=dff.iloc[selected_rows]
        color_col = "Desempeño" if "Desempeño" in dff.columns else None
        fig =px.scatter(dff,
                        x="Edad",
                        y="Promedio",
                        color=color_col,
                        size="Promedio",
                        title="Analisis detallado (Seleccione filas de la tabla)",
                        trendline="ols"if len(dff) > 1 else None
                        )
        return fig


 
# ejecutar la app
if __name__ == '__main__':
    appnotas.run(debug=True)
    print(df)