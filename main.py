import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("TSP Projection Dashboard", style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.Label("Current Age:"),
            dcc.Input(id='current_age', type='number', value=30, style={'marginRight': '10px'}),
            html.Label("Current TSP Balance:"),
            dcc.Input(id='current_balance', type='number', value=50000, style={'marginRight': '10px'}),
            html.Label("Annual Contribution:"),
            dcc.Input(id='annual_contribution', type='number', value=5000, style={'marginRight': '10px'}),
            html.Label("Annual Rate of Return (in %):"),
            dcc.Input(id='annual_return', type='number', value=7, style={'marginRight': '10px'}),
            html.Label("Projection Years:"),
            dcc.Input(id='years', type='number', value=20),
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    ]),
    dcc.Graph(id='tsp_projection_graph')
], style={'width': '50%', 'margin': '0 auto'})

# Callback to update the graph based on inputs
@app.callback(
    Output('tsp_projection_graph', 'figure'),
    [Input('current_age', 'value'),
     Input('current_balance', 'value'),
     Input('annual_contribution', 'value'),
     Input('annual_return', 'value'),
     Input('years', 'value')]
)
def update_graph(current_age, current_balance, annual_contribution, annual_return, years):
    # Calculate the projected balance
    years_range = np.arange(1, years + 1)
    ages = current_age + years_range
    balance = [current_balance]
    for year in years_range:
        balance.append(balance[-1] * (1 + annual_return / 100) + annual_contribution)

    # Create a DataFrame
    df = pd.DataFrame({
        'Age': ages,
        'Projected Balance': balance[1:]
    })

    # Create the graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Age'], y=df['Projected Balance'], mode='lines+markers', 
                             name='TSP Balance', line=dict(color='blue', width=2)))
    fig.update_layout(title='Projected TSP Balance Over Time',
                      xaxis_title='Age',
                      yaxis_title='Projected Balance',
                      plot_bgcolor='white',
                      font=dict(family="Arial, sans-serif", size=14, color="black"))

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
