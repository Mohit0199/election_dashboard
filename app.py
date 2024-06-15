import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load data
advertisers = pd.read_csv('advertisers.csv')
merged_data = pd.read_csv('merged_data.csv')

advertisers['Amount spent (INR)'] = pd.to_numeric(advertisers['Amount spent (INR)'], errors='coerce')
party_ad_spend = advertisers.groupby('Page name')[['Amount spent (INR)', 'Number of ads in Library']].sum().sort_values(by='Amount spent (INR)', ascending=False)
top_10 = party_ad_spend.head(10)

all_states = merged_data.groupby(['State']).agg({'Total Electors':'sum', 'Polled (%)':'mean', 'Total Votes':'sum', 'Amount spent (INR)':'first'})
state_dfs = {state: df for state, df in merged_data.groupby('State')}

all_phases = merged_data.groupby(['Phase']).agg({'Total Electors':'sum', 'Polled (%)':'mean', 'Total Votes':'sum', 'Amount spent (INR)':'first'})
phase_dfs = {phase: df for phase, df in merged_data.groupby('Phase')}

# Initialize Dash app with external stylesheet
external_stylesheets = [
    {
        "href": "https://cdn.jsdelivr.net/npm/bootswatch@5.0.0-alpha2/dist/spacelab/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-dZQ/D1fIe9SP9LH3snDLM/iAhOA1NVPpHCBfR5eJDIkNT+4UwGqX+8I0UD+OCQQ4",
        "crossorigin": "anonymous",
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Create the Top 10 ad spend
fig = px.bar(top_10, x=top_10.index, y='Amount spent (INR)',
             labels={'x': 'Page Name', 'Amount spent (INR)': 'Amount Spent (INR)'},
             template="plotly_dark")

fig.update_layout(
    xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
    yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
    )


# Define layout
app.layout = html.Div([
    html.H1("Election Advertising and Voting Analysis Dashboard",style={'color': '#fff', 'text-align': 'center', 'fontSize':'50'}),

    html.P(' Welcome to the Election Advertising and Voting Analysis Dashboard for the General Election of India 2024.This dashboard provides a comprehensive overview of the election, focusing on various key aspects:',
           style={'color': '#fff','font-family': 'Arial', 'font-size': '22px', 'marginTop': 50}),

    html.Div([
        html.P("Advertising Spend by Parties: Track the amount spent on advertisements by different political parties"),
        html.P("Voter Analysis: Analyze voter turnout and behavior across different states and phases of the election."),
        html.P("Total Electors and Votes Polled: View data on the total number of registered voters and the percentage of votes polled.")
    ], style={'color': '#fff','font-family': 'Arial', 'font-size': '18px'}),

    html.Div([
        html.H3("Data Information", style={'marginTop': 50}),
        html.P("State: The name of the state."),
        html.P("PC_Name: The name of the parliamentary constituency."),
        html.P("Total Electors: The total number of registered voters."),
        html.P("Polled (%): The percentage of votes polled."),
        html.P("Total Votes: The total number of votes cast."),
        html.P("Phase: The phase of the election."),
        html.P("Amount spent (INR): The total amount of money spent on ads in that location in Indian Rupees.")
    ], style={'color': '#fff','font-family': 'Arial', 'font-size': '18px'}),

    html.H2("Top 10 Advertisers by Ad Spend", style={'color': '#fff', 'marginTop': 50, 'font-size': '35px'}),
    dcc.Graph(id='top-10-advertisers', figure=fig, style={'background-color': '#ecf0f1'}),
    
    html.H1("State wise Data", style={'color': '#fff', 'marginTop': 50, 'font-size': '40px'}),
    html.H2("Select State", style={'color': '#fff', 'marginTop': 50, 'font-size': '25px'}),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': state, 'value': state} for state in state_dfs.keys()],
        value='All',
        multi=False,
        style={'width': '50%', 'marginBottom': 30}
    ),
    html.Div(id='state-graphs-container', style={'background-color': '#ecf0f1'}),


    html.H1("Phase wise Data", style={'color': '#fff', 'marginTop': 50, 'font-size': '40px'}),
    html.H2("Select Phase", style={'color': '#fff', 'marginTop': 50, 'font-size': '25px'}),
    dcc.Dropdown(
        id='phase-dropdown',
        options=[{'label': 'All', 'value': 'All'}] + [{'label': phase, 'value': phase} for phase in all_phases.index],
        value='All',
        multi=False,
        style={'width': '50%', 'marginBottom': 30}
    ),
    html.Div(id='phase-graphs-container', style={'background-color': '#ecf0f1'}),

])

app.title = "General Election 2024 Dashboard"

@app.callback(
    Output('state-graphs-container', 'children'),
    Input('state-dropdown', 'value')
)
def update_state_graphs(selected_state):
    graphs = []
    
    if selected_state == 'All':
        fig1 = px.bar(all_states, x=all_states.index, y='Polled (%)',
                          title="Votes Polled (All States)",
                          hover_data=['Total Votes'],
                          labels={'State': 'State', 'Polled (%)': 'Votes Polled (%)'},
                          template="plotly_dark")
        fig1.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        fig2 = px.bar(all_states, x=all_states.index, y='Total Electors',
                          title="Total Electors (All States)",
                          labels={'State': 'State', 'Total Electors': 'Total Electors'},
                          template="plotly_dark")
        fig2.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        fig3 = px.bar(all_states, x=all_states.index, y='Amount spent (INR)',
                          title="Total Amount Spent On Ads (All States)",
                          labels={'State': 'State', 'Amount spent (INR)': 'Amount spent (INR)'},
                          template="plotly_dark")
        fig3.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        graphs.extend([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2, style={'marginTop': 50}),
            dcc.Graph(figure=fig3, style={'marginTop': 50}),
            html.Hr()
        ])

    else:
        state_data = state_dfs.get(selected_state)
        
        fig1 = px.bar(state_data, x='PC_Name', y='Polled (%)',
                          title=f"Votes Polled - {selected_state}",
                          hover_data=['Total Votes'],
                          labels={'PC_Name': 'Parliamentary Constituency', 'Polled (%)': 'Votes Polled (%)'},
                          template="plotly_dark")
        fig1.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        fig2 = px.bar(state_data, x='PC_Name', y='Total Electors',
                          title=f"Total Electors - {selected_state}",
                          labels={'PC_Name': 'Parliamentary Constituency', 'Total Electors': 'Total Electors'},
                          template="plotly_dark")
        fig2.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        graphs.extend([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2, style={'marginTop': 50}),
            html.Hr()
        ])
    
    return graphs


@app.callback(
    Output('phase-graphs-container', 'children'),
    Input('phase-dropdown', 'value')
)
def update_phase_graphs(selected_phase):
    graphs = []
    
    if selected_phase == 'All':
        fig1 = px.bar(all_phases, x=all_phases.index, y='Polled (%)',
                          title="Votes Polled (All Phases)",
                          hover_data=['Total Votes'],
                          labels={'Phase': 'Phase', 'Polled (%)': 'Votes Polled (%)'},
                          template="plotly_dark")
        fig1.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        fig2 = px.bar(all_phases, x=all_phases.index, y='Total Electors',
                          title="Total Electors (All Phases)",
                          labels={'Phase': 'Phase', 'Total Electors': 'Total Electors'},
                          template="plotly_dark")
        fig2.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        fig3 = px.bar(all_phases, x=all_phases.index, y='Amount spent (INR)',
                          title="Total Amount Spent On Ads (All Phases)",
                          labels={'Phase': 'Phase', 'Amount spent (INR)': 'Amount spent (INR)'},
                          template="plotly_dark")
        fig3.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        graphs.extend([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2, style={'marginTop': 50}),
            dcc.Graph(figure=fig3, style={'marginTop': 50}),
            html.Hr()
        ])

    else:
        phase_data = phase_dfs.get(selected_phase).groupby('State').agg({'Total Electors':'sum', 'Polled (%)':'mean', 'Total Votes':'sum', 'Amount spent (INR)':'first'})
        
        fig1 = px.bar(phase_data, x=phase_data.index, y='Polled (%)',
                          title=f"Votes Polled - Phase {selected_phase}",
                          hover_data=['Total Votes'],
                          labels={'Phase': 'State', 'Polled (%)': 'Votes Polled (%)'},
                          template="plotly_dark")
        fig1.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        fig2 = px.bar(phase_data, x=phase_data.index, y='Total Electors',
                          title=f"Total Electors - Phase {selected_phase}",
                          labels={'Phase': 'State', 'Total Electors': 'Total Electors'},
                          template="plotly_dark")
        fig2.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        fig3 = px.bar(phase_data, x=phase_data.index, y='Amount spent (INR)',
                          title=f"Total Amount Spent On Ads - Phase {selected_phase}",
                          labels={'Phase': 'State', 'Amount spent (INR)': 'Amount spent (INR)'},
                          template="plotly_dark")
        fig3.update_layout(
            title={'font': {'size': 30, 'color': '#fff'}},
            xaxis={'title': {'font': {'size': 18, 'color': '#fff'}}},
            yaxis={'title': {'font': {'size': 18, 'color': '#fff'}}}
        )
        
        graphs.extend([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2, style={'marginTop': 50}),
            dcc.Graph(figure=fig3, style={'marginTop': 50}),
            html.Hr()
        ])
    
    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)
