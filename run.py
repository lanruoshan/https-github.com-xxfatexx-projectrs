#dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

# get Data
df = pd.read_csv ("Tech.csv" )

#get industry number
available_indicators = df['name'].unique()


#layout
app.layout = html.Div([
         html.Div([html.Label('Industry'),
     dcc.Dropdown(
       id='industry',
         options=[
             {'label': 'Tech', 'value': 'Tech'},
             {'label': 'Car', 'value': 'Car'},
             {'label': 'Bank', 'value': 'Bank'},

         ],
        value='Tech'
    )],style={'width': '20%', 'display': 'inline-block','position':'absolute','top':'250','left':'50','color': 'CornflowerBlue'

              }),

         html.Div([
            html.Label('Price Type'),
            dcc.Dropdown(
             id='priceType',
         options=[
             {'label': 'open', 'value': 'open'},
             {'label': 'close', 'value': 'close'},
             {'label': 'high', 'value': 'high'},
             {'label': 'low', 'value': 'low'},

         ],
         value='open'
     )],style={'width': '20%', 'display': 'inline-block','position':'absolute','top':'350','left':'50','color': 'CornflowerBlue '}),
         html.Div([dcc.RadioItems(

                id='graphType',
                options=[{'label': i, 'value': i} for i in ['Line', 'Bar','Scatter']],
                value='Line',
                labelStyle={'display': 'inline-block', 'textAlign': 'center'}
            )],style={'width': '75%', 'float': 'right', 'display': 'inline-block','position':'absolute','top':'450',
                   'left':"50"}),

         html.Div([dcc.Graph(

        id='example-graph',

        figure={

            'data': [
                go.Scatter(
                    x=df[df['name'] == i]['date'],
                    y=df[df['name'] == i]['open'],
                    text=df[df['name'] == i]['name'],
                    mode='lines+markers',  #scatter/ no--line
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.name.unique()
            ],

            'layout': go.Layout(

                xaxis={'title': 'date'},
                yaxis={'title': 'Open price'},
                #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},

                hovermode='closest'
            )}
         )],style={'width': '75%', 'float': 'right', 'display': 'inline-block','position':'absolute','top':'100',
                   'right':"1"})

        ])


@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('industry', 'value'),
     dash.dependencies.Input('priceType', 'value'),
     dash.dependencies.Input('graphType','value')])

def update_graph(industry,priceType,graphType):
    dff = pd.read_csv(industry + '.csv')
    if graphType == 'Bar':
        return {
            'data': [

                go.Bar(
                    x=dff[dff['name'] == i]['date'],
                    y=dff[dff['name'] == i][priceType],
                    text=dff[dff['name'] == i]['name'],

                    #mode='markers',  #scatter/ no--line


                    name=i
                ) for i in dff.name.unique()
            ],
            'layout': go.Layout(
                title=industry + ' Stock Price',
                xaxis={'title': 'date'},
                yaxis={'title': priceType+' price'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},

                hovermode='closest'
            )

        }
    elif graphType == 'Scatter':
        return {
            'data': [

                go.Scatter(
                    x=dff[dff['name'] == i]['date'],
                    y=dff[dff['name'] == i][priceType],
                    text=dff[dff['name'] == i]['name'],

                    mode='markers',  #scatter/ no--line

                    name=i
                ) for i in dff.name.unique()
            ],
            'layout': go.Layout(
                title=industry + ' Stock Price',
                xaxis={'title': 'date'},
                yaxis={'title': priceType+' price'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},

                hovermode='closest'
            )
        }
    else:
        return {
            'data': [

                go.Scatter(
                    x=dff[dff['name'] == i]['date'],
                    y=dff[dff['name'] == i][priceType],
                    text=dff[dff['name'] == i]['name'],

                    # mode='markers',  #scatter/ no--line

                    name=i
                ) for i in dff.name.unique()
            ],
            'layout': go.Layout(
                title= industry + ' Stock Price',
                xaxis={'title': 'date'},
                yaxis={'title': priceType+' price'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},

                hovermode='closest'
            )

        }

server = app.server
if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix

    server.wsgi_app = ProxyFix(server.wsgi_app)
    app.run_server(debug=True,host='0.0.0.0')

