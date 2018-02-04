import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
import os
from random import randint
import duo2 as duo
import plotly.graph_objs as go


sapp = dash.Dash(__name__)
server = app.server



app.layout = html.Div(children=[
    dcc.Graph(
        figure = go.Figure(
            data = data,
            layout = layout,
            ),
    style={'height': 300,
           'margin-top':0},
    id='my-graph'
    ),

html.Div(
    dcc.Graph(
        figure = go.Figure(
            data = data2,
            layout = layout2
            ),
        style={'height': 300},
        id='my-graph2'
        ),
    style = {'align':'left',
           'margin-left':400,
           'margin-top':-300}
),

html.Div(
    dcc.Graph(
        figure = go.Figure(
            data = data3,
            layout = layout3
            ),
        style={'height': 300},
        id='my-graph3'
        ),
    style = {'align':'left',
           'margin-left':800,
           'margin-top':-300}
),
html.P('Most Productive Attacking Partnerships',
        style = {'fontFamily':'Arial',
                 'fontSize':20,
                 'fontWeight':'bold',
                 'z-index': -1,
                 'position':'relative',
                 'margin-top':-285,
                 'margin-left':60}),
html.P('Partnerships with the most chances',
        style = {'fontFamily':'Arial',
                 'fontSize':13,
                 #'fontWeight':'bold',
                 'z-index': 2,
                 'position':'relative',
                 'margin-top':-17,
                 'margin-left':60}),
html.P('@FootyNumb3rs',
        style = {'fontFamily':'Arial',
                 'color':'grey',
                 'fontSize':15,
                 #'fontWeight':'bold',
                 'z-index': 2,
                 'position':'relative',
                 'margin-top':-8.5,
                 'margin-left':1119})

],
style = {'background-color':'#f1f1f1', 'width':1300,'height':1000,'margin-top':0})

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)

'''
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
'''