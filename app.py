# data manipulation
import pandas as pd

# plotly 
import plotly.express as px
import plotly.graph_objects as go

import base64

# dashboards
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc 
from datetime import date

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) 

data = pd.read_excel('dataOECD1980.xlsx', index_col=0)
data = data.rename(columns = {'LOCATION':'Location', 'FertilityRate': 'Fertility Rate', 'ChildSupport': 'Public Spending on Family Benefits', 
    'WomenSelfEmployed': 'Women Self-Employed','MarriageRate':'Marriage Rate'})

fert=pd.read_excel('dataOECD1980.xlsx')
fert2=fert.groupby('TIME')[['FertilityRate']].mean()
image_filename = 'baby5456.png' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

year_slider = dcc.Slider(
        id='year-slider',
        min=data['TIME'].min(),
        max=data['TIME'].max(),
        value=data['TIME'].max(),     
        marks={str(year): str(year) for year in data['TIME'].unique()},
        step=1
    )


_kpi1 = round(len(data['Country'].unique()), 2)
    

_kpi2 = round(data['Fertility Rate'][data['TIME']==2019].median(), 2)

_kpi3=[]
_kpi3.append(round(data['Fertility Rate'][data['TIME']==2019].min(), 2))
_kpi3.append(" ")
_kpi3.append(",")
_kpi3.append(" ")
_kpi3.append(round(data['Fertility Rate'][data['TIME']==2019].max(), 2))


# Tab 1

tab1_content = html.Div(
    [
        dbc.Card(                                 
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Label(
                                "Select Year:",
                                style={"font-size": "20px"},
                            ),
                            dbc.Col(year_slider, align="center"),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="graph-with-slider12"
                                ),
                                sm=6,
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id="graph-with-slider10"
                                ),
                                sm=6,
                            )
                        ],
                        align="center",),
                        dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="graph-with-slider11"
                                ),
                                sm=6,
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id="graph-with-slider13"
                                ),
                                sm=6,
                            )
                        ],
                        align="center",),
                ])
        ),

        dbc.Card(                                 
            dbc.CardBody(
                [
                    html.H1("Factors"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="graph-with-slider1"
                                ),
                                sm=6,
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id="graph-with-slider2"
                                ),
                                sm=6,
                            )
                        ],
                        align="center",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="graph-with-slider7"
                                ),
                                sm=6,
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id="graph-with-slider8"
                                ),
                                sm=6,
                            ),
                        ],
                        align="center",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="graph-with-slider9"
                                ),
                                sm=12,
                            )
                        ],
                        align="center",
                    ),
                    html.P('Definitions of the Factors:'),
                    html.Ol([   
                        html.Li('GDP (measured in US dollar per capita): the standard measure of the value added created through the production of goods and services in a \
                            country during a certain period. It also measures the income earned from that production, or the total \
                                amount spent on final goods and services (less imports).'),                
                        html.Li('Women Self-Employed: (measured by gender as percentage of total employment) those who are self-employed with employees are \
                            people whose primary activity is self-employment and who employ others.'),         
                        html.Li('Public Spending on Family Benefits (measured in percentage of GDP): includes financial support that is exclusively for families and children. \
                            There are three types of public spending on family benefits: child-related cash transfers (cash benefits) to families with children,\
                                Public spending on services for families (benefits in kind) with children, \
                                    Financial support for families provided through the tax system.'),
                        html.Li('Marriage Rate: (measured by percentage) the number of marriages during the year per 1000 people.')
                    ])
                ]
            ),
        )
    ]
)


# Tab 2

tab2_content = html.Div([html.Div(
    
    children=[
    dbc.Label(
            "Choose one of the following countries:",
            style={"font-size": "20px"},
            ),
    dcc.Dropdown(
        id='country select',
        options=[
            {'label': country , 'value': country }
                for country in data['Country'].unique()],
        value='United States' 
    ),

    html.Br(),

    html.Div(children=[   
    dbc.Label(
            "Select Year Range:",
            style={"font-size": "20px"},
            ),
    dcc.RangeSlider(
    id='crossfilter-year--slider',
    min=data['TIME'].min(),
    max=data['TIME'].max(),
    value=[data['TIME'].min(),data['TIME'].max()],
    marks={str(year): str(year) for year in data['TIME'].unique()},
    step=None    
)], style={'width': '100%'}),


html.Div([

html.Div(children=[
   dcc.Graph(id="line_plot"),
],style={'width': '70%', 'float': 'left', 'display': 'inline-block'}),


html.Div(children=[
     dcc.Loading(
                id='table-load',
                type='circle',
                children=[html.Div(id='summary-table-div',),]
            ),
html.Div([
            html.Br(),
            html.Br(),
            dbc.Card([
                dbc.CardHeader("Total Number of OECD Countries",class_name='text-center'),
                dbc.CardBody(
                    [
                    dcc.Loading(
                        id='kpi1-load',
                        type='dot',
                        children=[html.H4(_kpi1, className="text-center", id='kpi1'),])
                    ]
                ),
            ], color="#636EFA", inverse=True),

            dbc.Card([
                dbc.CardHeader("Median Fertility Rate of last selected year",class_name='text-center'),
                dbc.CardBody(
                    [
                        dcc.Loading(
                            id='kpi2-load',
                            type='dot',
                            children=[html.H4(_kpi2, className="text-center",  id='kpi2'),])
                    ]
                ),
            ], color="#E74C3C", inverse=True),

            dbc.Card([
                dbc.CardHeader("Min and Max Fertility Rate of last selected year",class_name='text-center'),
                dbc.CardBody(
                    [
                        dcc.Loading(
                                    id='kpi3-load',
                                    type='dot',
                                    children=[html.H4(_kpi3, className="text-center", id='kpi3'),])
                    ]
                ),
            ], color="#636EFA", inverse=True),
        ])
    ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'}),

])
],style={'width': '97%','float': 'left', 'display': 'inline-block'}),

html.H1("Factors"),
html.Hr(),

html.Div([
    dcc.Graph(
        id='GDP_graph',
    )
], 
    style={'width': '50%', 'display': 'inline-block', 'padding': '0 10'}),

html.Div([
    dcc.Graph(
        id='WSE_graph',
    )
], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),

html.Div([
    html.Div([
    dcc.Graph(
        id='CS_graph',
    )
], 
    style={'width': '50%', 'display': 'inline-block', 'padding': '0 10'}),

html.Div([
    dcc.Graph(
        id='MR_graph',
    )
], style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),

                html.P('Definitions of the Factors:'),
                html.Ol([   
                        html.Li('GDP (measured in US dollar per capita): the standard measure of the value added created through the production of goods and services in a \
                            country during a certain period. It also measures the income earned from that production, or the total \
                                amount spent on final goods and services (less imports).'),                
                        html.Li('Women Self-Employed: (measured by gender as percentage of total employment) those who are self-employed with employees are \
                            people whose primary activity is self-employment and who employ others.'),         
                        html.Li('Public Spending on Family Benefits (measured in percentage of GDP): includes financial support that is exclusively for families and children. \
                            There are three types of public spending on family benefits: child-related cash transfers (cash benefits) to families with children,\
                                Public spending on services for families (benefits in kind) with children, \
                                    Financial support for families provided through the tax system.'),
                        html.Li('Marriage Rate: (measured by percentage) the number of marriages during the year per 1000 people.')
                ])
])])

                
app.layout = html.Div(
    [
        html.H1('Fertility Rate in OECD Countries'),
        html.P('Dashboard created by Krish Vora, Leah Xia, Lesly Liu, Rakshit Jha, Spencer Wang'),
        html.Br(),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={'height':'50%','width':'100%'}),
                    html.H1(' ',
                        style={'color': 'gray',
                        'fontSize': '40px'}),
        html.Br(),
        dcc.Tabs([
                dcc.Tab(tab1_content, label="OECD Members"),
                dcc.Tab(tab2_content, label="Each Country")
            ],
            colors={
                    "border": "#6495ED",
                    "primary": "#6495ED",
                    "background": "#6495ED"
            }
        )
    ]
)



# for first tab

@app.callback(
    dash.dependencies.Output('graph-with-slider12', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])

def function(year):
    fig = go.Figure(data=go.Choropleth(
        locations=fert.loc[fert['TIME']==year,]['LOCATION'], 
        z = fert.loc[fert['TIME']==year,]['FertilityRate'].astype(float), 
        colorscale = 'RdBu',
        colorbar_title = "Fercility Rate",
    ))

    fig.update_layout(
        geo_scope='world', 
         title={
        'text': "Fertility Rate in Map View"
    },
    )
    return fig

@app.callback(
 dash.dependencies.Output('graph-with-slider10', 'figure'),
 [dash.dependencies.Input('year-slider', 'value')])

def function(year):
    fig = px.line(x = fert2.loc[1980:year,].index,
    y = fert2.loc[1980:year,]['FertilityRate'],
    labels= {'y': 'Fertility Rate (%)','x':'Year'},
    width = 680, height= 500)
    fig.update_xaxes(type='category',dtick=1)
    fig.update_layout(
    title={
    'text': "Trend of Fertility Rate" 
    })
    return fig


@app.callback(
 dash.dependencies.Output('graph-with-slider11', 'figure'),
 [dash.dependencies.Input('year-slider', 'value')])

def function(year):
    fig = go.Figure()
    fert_r = fert.loc[fert['TIME']==year].sort_values('FertilityRate', ascending=True).reset_index()
    fig.add_trace(go.Scatter(x = fert_r['FertilityRate'],
                            y = fert_r['Country'],
                            mode = 'markers',
                            marker_color ='#636EFA',
                            marker_size  = 7))
    for i in range(0, fert_r.shape[0]):
                fig.add_shape(type='line',
                                x0 = 0, y0 = i,
                                x1 = fert_r['FertilityRate'][i],
                                y1 = i,
                                line=dict(color='#636EFA', width = 1))
    fig.update_layout(title_text = "Fertility Rate in " + str(year),
                    height= 900,
                    xaxis_title="Fertility Rate (%)",
                    yaxis_title="Countries")
    return fig

@app.callback(
 dash.dependencies.Output('graph-with-slider13', 'figure'),
 [dash.dependencies.Input('year-slider', 'value')])

def function(year):
    fert_year= fert.loc[fert['TIME']==year]
    fig = px.violin(fert_year, y="FertilityRate", box=True, # draw box plot inside the violin
                    # points='all', # can be 'outliers', or False
                )
    fig.update_layout(title_text = "Distribution of Fertility Rate in " +str(year) , height = 850,
                    yaxis_title="Fertility Rate (%)")
    return fig
   

@app.callback(
    [
        Output(component_id="graph-with-slider1", component_property="figure"),
        Output(component_id="graph-with-slider2", component_property="figure"),
        Output(component_id="graph-with-slider7", component_property="figure"),
        Output(component_id="graph-with-slider8", component_property="figure"),
        Output(component_id="graph-with-slider9", component_property="figure")
    ],
    Input('year-slider', 'value'))        

def update_figure(year):                         
    data_year = data.loc[data['TIME']== year]    

    fig1 = px.scatter(data_year, x = "Public Spending on Family Benefits", y = "Fertility Rate", trendline="ols", trendline_color_override="red")
    fig1.update_layout(title="Fertility Rate vs Public Spending on Family Benefits", title_x=0.5,
                  xaxis_title="Public Spending on Family Benefits (%)",
                  yaxis_title="Fertility Rate (%)")

    fig2 = px.scatter(data_year, x = "GDP", y = "Fertility Rate",  trendline="ols", trendline_color_override="red")
    fig2.update_layout(title="Fertility Rate vs GDP ", title_x=0.5,
                  xaxis_title="GDP (USD/Capita)",
                  yaxis_title="Fertility Rate (%)")

    fig7 = px.scatter(data_year, x = "Women Self-Employed", y = "Fertility Rate", trendline="ols", trendline_color_override="red")
    fig7.update_layout(title="Fertility Rate vs Women Self-Employed", title_x=0.5,
                  xaxis_title="Women Self-Employed (%)",
                  yaxis_title="Fertility Rate (%)")

    fig8 = px.scatter(data_year, x = "Marriage Rate", y = "Fertility Rate", trendline="ols", trendline_color_override="red")
    fig8.update_layout(title="Fertility Rate vs Marriage Rate", title_x=0.5,
                  xaxis_title="Marriage Rate (%)",
                  yaxis_title="Fertility Rate (%)")

    fig9 = go.Figure(data=[go.Table(
    header=dict(values=list(data_year.columns[[11, 2, 3, 4, 9, 10]])
                ),
    cells=dict(values=[data_year.round(2)[i] for i in data_year.columns[[11, 2, 3, 4, 9, 10]]]
               ))
    ])
    fig9.update_layout(title="Detailed Data", title_x=0.5)


    return fig2, fig7, fig1, fig8, fig9


# for second tab

@app.callback(
    dash.dependencies.Output("GDP_graph", "figure"), 
    [dash.dependencies.Input("country select", "value"),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def GDP_create(country,year_value):
    data = pd.read_excel('dataOECD1980_country.xlsx')
    data['Year'] = data['TIME'].astype('str')
    data1=data[(data['TIME'] >= year_value[0]) & (data['TIME'] <= year_value[1])]
    fig = px.scatter(data1[data1['Country']==country], y='FertilityRate', x='GDP', color='Year', trendline='ols', trendline_color_override= 'red')
    fig.update_layout(
    title={
        'text': "Fertility Rate vs GDP",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="GDP (USD/Capita)",
        yaxis_title="Fertility Rate (%)")
    return fig

@app.callback(
    dash.dependencies.Output("WSE_graph", "figure"), 
    [dash.dependencies.Input("country select", "value"),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def WSE_create(country,year_value):
    data = pd.read_excel('dataOECD1980_country.xlsx')
    data['Year'] = data['TIME'].astype('str')
    data2=data[(data['TIME'] >= year_value[0]) & (data['TIME'] <=year_value[1])]
    fig = px.scatter(data2[data2['Country']==country], y='FertilityRate', x='WomenSelfEmployed', color='Year', trendline='ols', trendline_color_override= 'red')
    fig.update_layout(
    title={
        'text': "Fertility Rate vs Women Self-Employed",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="Women Self-Employed (%)",
        yaxis_title="Fertility Rate (%)")
    return fig

@app.callback(
    dash.dependencies.Output("CS_graph", "figure"), 
    [dash.dependencies.Input("country select", "value"),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def CS_create(country,year_value):
    data = pd.read_excel('dataOECD1980_country.xlsx')
    data['Year'] = data['TIME'].astype('str')
    data3=data[(data['TIME'] >= year_value[0]) & (data['TIME'] <=year_value[1])]
    fig = px.scatter(data3[data3['Country']==country], y='FertilityRate', x='ChildSupport',  color='Year', trendline='ols', trendline_color_override= 'red')
    fig.update_layout(
    title={
        'text': "Fertility Rate vs Public Spending on Family Benefits",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="Public Spending on Family Benefits (%)",
        yaxis_title="Fertility Rate (%)")
    return fig

@app.callback(
    dash.dependencies.Output("MR_graph", "figure"), 
    [dash.dependencies.Input("country select", "value"),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def MR_create(country,year_value):
    data = pd.read_excel('dataOECD1980_country.xlsx')
    data['Year'] = data['TIME'].astype('str')
    data4=data[(data['TIME'] >= year_value[0]) & (data['TIME'] <= year_value[1])]
    fig = px.scatter(data4[data4['Country']==country], y='FertilityRate', x='MarriageRate',  color='Year', trendline='ols', trendline_color_override= 'red')
    fig.update_layout(
    title={
        'text': "Fertility Rate vs Marriage Rate",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="Marriage Rate (%)",
        yaxis_title="Fertility Rate (%)")
    return fig


@app.callback(
    dash.dependencies.Output("line_plot", "figure"), 
    [dash.dependencies.Input("country select", "value"),
    dash.dependencies.Input('crossfilter-year--slider', 'value')])
def line_plot_create(country,year_value):
    data = pd.read_excel('dataOECD1980_country.xlsx')
    data1 = data[((data['Country'] == country) & (data['TIME'] >= year_value[0]) & (data['TIME'] <=year_value[1])) | ((data['Country'] == 'OECD Average') &
                    (data['TIME'] >= year_value[0]) & (data['TIME'] <=year_value[1]))]
    fig = px.line(data1, y='FertilityRate', x='TIME', color = 'Country')
    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.99
))  
    fig.update_layout(
    title={
        'text': "Fertility Rate vs Year",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        xaxis_title="Year",
        yaxis_title="Fertility Rate (%)")

    return fig

@app.callback(
    [Output("kpi1", "children"),
     Output("kpi2", "children"),
     Output("kpi3", "children"),
    ],
    [Input("crossfilter-year--slider", "value"),]
)
def update_kpis(year_value):
    data = pd.read_excel('dataOECD1980_country.xlsx')

    if year_value[1] == None:
        raise PreventUpdate
    
    kpi1 = round(len(data['Country'][data['TIME']==year_value[1]].unique())-1, 2)
    
    kpi2 = round(data['FertilityRate'][data['TIME']==year_value[1]].median(), 2)
    
    kpi3=[]
    kpi3.append(round(data['FertilityRate'][data['TIME']==year_value[1]].min(), 2))
    kpi3.append(" ")
    kpi3.append(",")
    kpi3.append(" ")
    kpi3.append(round(data['FertilityRate'][data['TIME']==year_value[1]].max(), 2))
    
    return kpi1, kpi2, kpi3
    


if __name__ == '__main__':
    app.run_server(debug=True)