
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import boto3
from dash import Dash, html, Input, Output, callback_context
import os
import numpy as np

#Im folgenden Abschnitt wird eine Funktion erstellt welche die aktuellsten Dateien der jeweiligen Shockboxxen heruntergeladen
# und Lokal als D1,..., D7 abgespeichert. Bei wiederholtem ausführen werden die Daten Überschrieben bzw aktualisiert
#-------------------------------------------------------------------------------------------------------
def download():
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket='wetterstationsbucket', Prefix='dataset/')
    objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'])
    latest_object = objects[-1]['Key']
    filename = latest_object[latest_object.rfind('/') + 1:]  # Remove path
    # Download in aktuellen ordner
    s3_client.download_file('wetterstationsbucket', latest_object, 'D1.csv')

    response = s3_client.list_objects_v2(Bucket='wetterstationsbucket', Prefix='d3/')
    objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'])
    latest_object = objects[-1]['Key']
    filename = latest_object[latest_object.rfind('/') + 1:]  # Remove path
    # Download in aktuellen ordner
    s3_client.download_file('wetterstationsbucket', latest_object, 'D3.csv')

    response = s3_client.list_objects_v2(Bucket='wetterstationsbucket', Prefix='d5/')
    objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'])
    latest_object = objects[-1]['Key']
    filename = latest_object[latest_object.rfind('/') + 1:]  # Remove path
    # Download in aktuellen ordner
    s3_client.download_file('wetterstationsbucket', latest_object, 'D5.csv')

    response = s3_client.list_objects_v2(Bucket='wetterstationsbucket', Prefix='d6/')
    objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'])
    latest_object = objects[-1]['Key']
    filename = latest_object[latest_object.rfind('/') + 1:]  # Remove path
    # Download in aktuellen ordner
    s3_client.download_file('wetterstationsbucket', latest_object, 'D6.csv')

    response = s3_client.list_objects_v2(Bucket='wetterstationsbucket', Prefix='d7/')
    objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'])
    latest_object = objects[-1]['Key']
    filename = latest_object[latest_object.rfind('/') + 1:]  # Remove path
    # Download in aktuellen ordner
    s3_client.download_file('wetterstationsbucket', latest_object, 'D7.csv')
    # -------------------------------------------------------------------------------------------------------------

download()
#Import & Sortieren der CSV-Datei nach Datum (D1)
#----------------------------------------------------------------------------------------
d1 = pd.read_csv('D1.csv')
#Sortieren der CSV-Datei nach Datum
d1['date'] = pd.to_datetime(d1.timestamp, infer_datetime_format=True)
d1.sort_values(by='date', ascending=True, inplace=True)
#Das gleiche mit Shockbox D3
d2 = pd.read_csv('D3.csv')
#Sortieren der CSV-Datei nach Datum
d2['date'] = pd.to_datetime(d2.timestamp, infer_datetime_format=True)
d2.sort_values(by='date', ascending=True, inplace=True)
#----------------------------------------------------------------------------------------
#Das gleiche mit Shockbox D5
d3 = pd.read_csv('D5.csv')
#Sortieren der CSV-Datei nach Datum
d3['date'] = pd.to_datetime(d3.timestamp, infer_datetime_format=True)
d3.sort_values(by='date', ascending=True, inplace=True)
#----------------------------------------------------------------------------------------

#Das gleiche mit Shockbox D6
d4 = pd.read_csv('D6.csv')
#Sortieren der CSV-Datei nach Datum
d4['date'] = pd.to_datetime(d4.timestamp, infer_datetime_format=True)
d4.sort_values(by='date', ascending=True, inplace=True)
#----------------------------------------------------------------------------------------

#Das gleiche mit Shockbox D7
d5 = pd.read_csv('D7.csv')
#Sortieren der CSV-Datei nach Datum
d5['date'] = pd.to_datetime(d5.timestamp, infer_datetime_format=True)
d5.sort_values(by='date', ascending=True, inplace=True)
#----------------------------------------------------------------------------------------

app = Dash(__name__)

app.layout = html.Div(children=[
    html.Div([
        html.H2("Datenvisualisierung der Shockboxen D1, D3, D5 & D7"),
        html.Img(src="/assets/banner1.png")
    ], className='banner'),
    html.Div([
        dcc.Dropdown(
            id='pandas-dropdown-1',
            value="temperature1",
            options=[
                {'label': 'Temperatur1', 'value': 'temperature1'},
                {'label': 'Temperatur2', 'value': 'temperature2'},
                {'label': 'Luftfeuchtigkeit', 'value': 'bmehum'},
                {'label': 'Batteriestatus', 'value': 'battery'},
                {'label': 'Event', 'value': 'event'}
            ]),
    ]),

    dcc.Graph(id='our_graph'),
    html.Div(id='pandas-output-container-1'),
    html.Div([
        html.Img(src="/assets/Ibatec.png")
    ]),
    html.Div([
        html.Button('Akrualisieren', id='btn-nclicks-1', n_clicks=0),
        html.Div(id='container-button-timestamp')
    ])
])

@app.callback(
    Output('pandas-output-container-1', 'children'),
    Input('pandas-dropdown-1', 'value')
)
def update_output(value):
    return f'Sie haben  {value} ausgewählt'


@app.callback(
    Output('our_graph', 'figure'),
    Input('pandas-dropdown-1', 'value')
    )
def update_graph(Auswahl):

    if Auswahl=='temperature1':
        line_fig = px.line(d1,
                       x='date', y='temperature1')
        line_fig.add_scatter(x=d2['timestamp'], y=d2['temperature1'], mode='lines', name='Shockbox D3')
        line_fig.add_scatter(x=d3['timestamp'], y=d3['temperature1'], mode='lines', name='Shockbox D5')
        line_fig.add_scatter(x=d4['timestamp'], y=d4['temperature1'], mode='lines', name='Shockbox D6')
        line_fig.add_scatter(x=d5['timestamp'], y=d5['temperature1'], mode='lines', name='Shockbox D7')
    if Auswahl=='temperature2':
        line_fig = px.line(d1,
                       x='date', y='temperature2')
        line_fig.add_scatter(x=d2['timestamp'], y=d2['temperature2'], mode='lines', name='Shockbox D3')
        line_fig.add_scatter(x=d3['timestamp'], y=d3['temperature2'], mode='lines', name='Shockbox D5')
        line_fig.add_scatter(x=d4['timestamp'], y=d4['temperature2'], mode='lines', name='Shockbox D6')
        line_fig.add_scatter(x=d5['timestamp'], y=d5['temperature2'], mode='lines', name='Shockbox D7')

    if Auswahl=='bmehum':
        line_fig = px.line(d1,
                       x='timestamp', y='bmehum')
        line_fig.add_scatter(x=d2['timestamp'], y=d2['bmehum'], mode='lines', name='Shockbox D3')
        line_fig.add_scatter(x=d3['timestamp'], y=d3['bmehum'], mode='lines', name='Shockbox D5')
        line_fig.add_scatter(x=d4['timestamp'], y=d4['bmehum'], mode='lines', name='Shockbox D6')
        line_fig.add_scatter(x=d5['timestamp'], y=d5['bmehum'], mode='lines', name='Shockbox D7')

    if Auswahl=='battery':
        line_fig = px.line(d1,
                       x='timestamp', y='battery')
        line_fig.add_scatter(x=d2['timestamp'], y=d2['battery'], mode='lines', name='Shockbox D3')
        line_fig.add_scatter(x=d3['timestamp'], y=d3['battery'], mode='lines', name='Shockbox D5')
        line_fig.add_scatter(x=d4['timestamp'], y=d4['battery'], mode='lines', name='Shockbox D6')
        line_fig.add_scatter(x=d5['timestamp'], y=d5['battery'], mode='lines', name='Shockbox D7')


    if Auswahl=='event':
        line_fig = px.line(d1,
                       x='timestamp', y='event')
        line_fig.add_scatter(x=d2['timestamp'], y=d2['event'], mode='lines', name='Shockbox D3')
        line_fig.add_scatter(x=d3['timestamp'], y=d3['event'], mode='lines', name='Shockbox D5')
        line_fig.add_scatter(x=d4['timestamp'], y=d4['event'], mode='lines', name='Shockbox D6')
        line_fig.add_scatter(x=d5['timestamp'], y=d5['event'], mode='lines', name='Shockbox D7')

    return line_fig

@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks')
)
def displayClick(btn1):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        download(),
        msg = 'Die Graphen werden aktualisiert. Die Shockbox liefert in einem Intervall von 15 min Daten. Graphen werden nur in diesem Intervall aktualisiert.----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'


    return html.Div(msg)

if __name__ == '__main__':
    app.run_server(debug=True)
