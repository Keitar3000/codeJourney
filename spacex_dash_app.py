import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Assuming spacex_df is a DataFrame containing launch site data
spacex_df = pd.read_csv('spacex_launch_dash.csv')

# Create Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define layout
app.layout = html.Div([
    # Dropdown for launch site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
        ],
        value='All Sites',  # Default value
        placeholder="Select a launch site",
        searchable=True
    ),
    html.Br(),

    # Pie chart for success count
    html.Div(id='success-pie-chart'),
    html.Br(),

    # Scatter plot for success vs. payload
    dcc.Graph(id='success-payload-scatter-chart'),  # Assigning the id directly to dcc.Graph component

    html.Br(),

    # Slider for payload range
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[0, 10000],  # Default value
        marks={i: str(i) for i in range(0, 10001, 1000)}
    )
])

# Define callback for updating pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='children'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'All Sites':
        # Calculate total successful launches for all sites
        success_counts = spacex_df[spacex_df['class'] == 1]['Launch Site'].value_counts()
        labels = success_counts.index.tolist()
        values = success_counts.tolist()
        title = 'Total Successful Launches for All Sites'
    else:
        # Calculate success vs. failed counts for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_counts = site_data[site_data['class'] == 1]['class'].count()
        failed_counts = site_data[site_data['class'] == 0]['class'].count()
        labels = ['Successful', 'Failed']
        values = [success_counts, failed_counts]
        title = f'Success vs. Failed Counts for {entered_site}'

    # Create pie chart
    fig = px.pie(
        values=values,
        names=labels,
        title=title
    )

    return dcc.Graph(figure=fig)


# Define callback for updating scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    if entered_site == 'All Sites':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation between Payload and Success for All Sites')
    else:
        site_data = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = site_data[(site_data['Payload Mass (kg)'] >= payload_range[0]) & 
                                (site_data['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Correlation between Payload and Success for {entered_site}')

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
