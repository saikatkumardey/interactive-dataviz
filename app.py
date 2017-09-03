import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv("iris.csv")
df_long = pd.melt(df,id_vars=['species'])

app = dash.Dash('')
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([

        html.Div([
                html.H2("Species"),
                dcc.Checklist(
                    id='species-type',
                    options=[{'label': i, 'value': i} for i in df_long.species.unique()],
                    values=['setosa']),
                html.Hr(),
                html.H2("Variable"),
                dcc.RadioItems(id='column',
                               options=[{'label': i, 'value': i} for i in df_long.variable.unique()],
                               value='petal_length')
                ],
                 style={'width':'48%','display':'inline-block'}),

        html.Div([dcc.Graph(id='graph')],
                 style={'width':'48%','display':'inline-block','float':'right'})
        ])

@app.callback(dash.dependencies.Output('graph','figure'),
              [dash.dependencies.Input('species-type','values'),dash.dependencies.Input('column','value')])
def update_graph(species_types,column):
    return {
        'data': [
            go.Histogram(x= df_long[(df_long['species']==species) & (df_long['variable']==column)]['value'],
                         histnorm='probability',
                         opacity='0.75',
                         name=species)
            for species in species_types
            ],
        'layout': go.Layout(
            xaxis= {
                'title': column
            },
            yaxis= {
                'title': 'Frequency(normalized)'
            },
            barmode='overlay',
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode= 'closest',
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
