import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
from google.cloud import bigquery

client = bigquery.Client.from_service_account_json('app/scweb-325801-a43f2038549f.json')
project_id = 'scweb-325801'
query = '''
select DISTINCT NAME from weather_fdn.day_stat_part_date ORDER BY NAME
'''
df = client.query(query, project=project_id).to_dataframe()
stations = [{"value": x, "label": x} for x in list(df.NAME.values)]

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ]
)

layout = html.Div(
    [
        dcc.Dropdown(
                    id="select_station",
                    options=stations,
                    multi=True
                ),

        dbc.Spinner(dcc.Graph(id='fig_temp')),

        dbc.Spinner(dcc.Graph(id='fig_stat'))
    ]
)


# Update graph when city is selected
@app.callback(
    Output("fig_temp", "figure"),
    Output("fig_stat", "figure"),
    [Input("select_station", "value")]
)
def update_graph(stations):  
    fig_temp = go.Figure()
    fig_stat = go.Figure()
    if stations is not None:
        for station in stations:
            sql_text = f"""
                        select * 
                        from weather_fdn.day_stat_part_date
                        WHERE NAME = '{station}'
            """
            df = client.query(sql_text, project=project_id).to_dataframe()
            df.DATE = pd.to_datetime(df.DATE)
            df = df.sort_values(by='DATE')
            df.set_index('DATE', inplace=True)
            df['C'] = (df['TEMP']-32)*5.0/9.0
            fig_temp.add_trace(go.Scatter(x=df.index, y=df.C, name=station))

            # month-statistic
            sql_text = f"""
                        select extract(month FROM date) m, AVG((TEMP-32)*5.0/9.0) TEMP
                        from weather_fdn.day_stat_part_date
                        WHERE NAME = '{station}'
                        GROUP BY m
                        ORDER BY m
            """
            df = client.query(sql_text, project=project_id).to_dataframe()
            fig_stat.add_trace(go.Bar(x=df.m, y=df.TEMP, name=station))

    fig_temp.update_layout(legend=dict(orientation="h"), 
                            title={
                                    'text': 'Temperature',
                                    },
                            margin=dict(l=50, r=10, t=80, b=20),     
                            title_font = dict(size=24),
                            title_x = 0.05,
                            )

    fig_stat.update_layout(legend=dict(orientation="h"), 
                            title={
                                    'text': 'Month statistic',
                                    },
                            margin=dict(l=50, r=10, t=80, b=20),     
                            title_font = dict(size=24),
                            title_x = 0.05,
                            )

    return fig_temp, fig_stat

if __name__ == "__main__":
    app.layout = layout
    app.title = 'World weather' 
    app.run_server(
        host='0.0.0.0',
        port=8050,
        debug=False
    )