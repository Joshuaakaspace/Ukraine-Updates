from dash import Dash, html, dcc, Input, Output, callback  
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  

dfc = pd.read_csv("Uk6.csv")
# dfp = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Analytic_Web_Apps/VizForGood/Scatter_mapbox/Sunny%20Street%20-%20Patient%20data%203%20years.csv")

# Data Processing *********************************************************
# *************************************************************************
dfc["Activity"] = dfc["Activity"].replace(
    {
        "Hervey Bay Neighbourhood/ Community Centre ": "Hervey Bay Neighbourhood",
        "Maroochydore Neighbourhood Centre Community Event ": "Maroochydore Neighbourhood Centre",
    }
)

# create shift periods for the bottom map
dfc["Start Time"] = pd.to_datetime(dfc["Start Time"], format="%I:%M %p").dt.hour
dfc["shift_start"] = ""
dfc.loc[dfc["Start Time"] >= 19, "shift_start"] = "night"
dfc.loc[dfc["Start Time"] < 12, "shift_start"] = "morning"
dfc.loc[
    (dfc["Start Time"] >= 12) & (dfc["Start Time"] < 19), "shift_start"
] = "afternoon"
dfc_shift = dfc.groupby(["Latitude", "Longitude", "Activity", "shift_start"])[
    ["ROU"]
].sum()
dfc_shift.reset_index(inplace=True)
# print(dfc_shift.head())

# calculate average shift time for bottom histogram graph
avg_shift_time = round(dfc["Length minutes"].mean())

# re-organize dataframe for the top map
dfc_gpd = dfc.groupby(["Latitude", "Longitude", "Activity"])[
    [
       "ROU",
       "Death",
       "Nursing/Paramedic Consults",
       "Conversations about health education",
        "Allied Health",
       "Providing Refugee",
       "Service provider conversations",
       "Mental health",
       "Suicide prevention/planning",
       "Substance use",
       "Medication education",
       "Impacted Region",
       "Length minutes",
    ]
].sum()
dfc_gpd.reset_index(inplace=True)


app = Dash(
    __name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True , title="IOTE - Ukraine Updates"
)
server = app.server

# Layout building *********************************************************
app.layout = dbc.Container(
    [
        dbc.Container(
            [
                html.H1(
                    "Ukraine Live Updates",
                    style={"textAlign": "center"},
                    className="display-3",
                )
            ],
            className="p-5 bg-warning rounded-1 mt-3 mb-5",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Impacted City Conditions:"),
                        html.P(
                            "Change dropdown and button values to see the impacted regions."
                        ),
                        dcc.Dropdown(
                            id="bar-data",
                            clearable=False,
                            value="Activity",
                            options=[
                                {"label": "Impacted Region", "value": "Activity"},
                                {"label": "Region", "value": "Region"},
                            ],
                        ),
                    ],
                    width=5,
                ),
                dbc.Col(
                    [html.P("")],
                    style={
                        "borderLeft": "6px solid white",
                        "height": "600px",
                        "position": "absolute",
                        "left": "49.75%",
                    },
                ),
                dbc.Col(
                    [
                        html.H3("Regions Occupied"),
                        html.P(
                            "Kindly scroll to see the impacted regions."
                        ),
                        dcc.Dropdown(
                            id="map1-conslt-data",
                            clearable=False,
                            value="ROU",
                            options=[
                                {
                                    "label": "ROU",
                                    "value": "ROU",
                                },
                                #{
                                    #"label": "Deaths",
                                    #"value": "Deaths",
                                #},
                                {
                                    "label": "Countries Providing Refugee",
                                    "value": "Providing Refugee",
                                },
                                {"label": "Loss of City", 
                                "value": "Substance use"},
                            ],
                        ),
                    ],
                    width=5,
                ),
            ],
            justify="around",
        ),
        dbc.Row(
            [
                dbc.Col(id="bar-col", children=[], width=5),
                dbc.Col(id="map-conslt-col", children=[], width=5),
            ],
            justify="around",
            className="mb-3",
        ),
       

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Img(
                            #src="/assets/image3.jpg",
                            #src="logo 2.jpg",
                            style={"maxHeight": "500px", "maxWidth": "200px"},
                        )
                    ],
                    width=2,
                ),

                dbc.Col(
                    [
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.H6(
                        dcc.Markdown('''
                                    ### Live News From Ukraine:
                                    Headlines and Description:
                                    * U.S., G7 allies may strip Russia of 'most favored nation' status - Reuters.com
                                    * Description:
                                    > The United States, together with the Group of Seven nations and the European Union, will move on Friday to revoke Russia's "most favored nation" status over its invasion of Ukraine, multiple people familiar with the situation told Reuters.
                                    > Read full article:
                                    https://www.reuters.com/business/biden-call-an-end-normal-trade-relations-with-russia-increased-tariffs-russian-2022-03-11/
                                    * Inside the quiet US diplomacy to ramp down tensions with Saudis, UAE -- and ramp up oil production - CNN
                                    * Description:
                                    > An intense, closely guarded diplomatic effort by a core team of Biden energy and national security officials to raise global oil production amid surging prices from Russia's war in Ukraine has fostered a cautious sense of optimism inside the White House.
                                    > Read full article:
                                    https://www.cnn.com/2022/03/11/politics/oil-diplomacy-saudi-uae-tensions-russia-ukraine/index.html
                                    * Russia owes Western banks $120 billion. They won't get it back - CNN
                                    * Description:
                                    > Goldman Sachs and JPMorgan Chase are the first major Western banks to get out of Russia following the invasion of Ukraine. More are likely to follow at a cost of tens of billions of dollars.
                                    > Read full article:
                                    https://www.cnn.com/2022/03/10/investing/banks-russia-exposure/index.html
                                    * Russian strikes hit western Ukraine as offensive widens - The Associated Press - en Español
                                    * Description:
                                    > LVIV, Ukraine (AP) — Russia widened its military offensive in Ukraine on Friday, striking near airports in the west of the country for the first time, as observers and satellite photos indicated that its troops, long stalled in a convoy outside the capital Ky…
                                    > Read full article:
                                    https://apnews.com/be25927bc5eef0f90cf466a86fcc6e3f
                                    * Households squeezed as U.S. consumer prices accelerate; more pain coming - Reuters
                                    * Description:
                                    > U.S. consumer prices surged in February, forcing Americans to dig deeper to pay for rent, food and gasoline, and inflation is poised to accelerate even further as Russia's war against Ukraine drives up the costs of crude oil and other commodities.
                                    > Read full article:
                                    https://www.reuters.com/business/us-consumer-prices-accelerate-february-weekly-jobless-claims-rise-2022-03-10/
                                    * Global food shortage and higher prices may result from war in Ukraine - CNN
                                    * Description:
                                    > Global food challenges could worsen as a result of the Russian invasion of Ukraine, leading to shortages and higher food prices. The World Food Programme has lost access to a key source of grain from Ukraine, a major food exporter known as the "bread basket o…
                                    > Read full article:
                                    https://www.cnn.com/videos/business/2022/03/10/food-prices-crisis-russia-ukraine-invasion-qmb-vpx.cnnbusiness
                                    * War in Ukraine: Is the party over for Chelsea? - Sky News
                                    * Description:
                                    > The future of Chelsea is uncertain after the government froze the assets of the Russian oligarch Roman Abramovich.Culture Secretary Nadine Dorries said Abram...
                                    > Read full article:
                                    https://www.youtube.com/watch?v=Uqi60RXj3DQ
                                ''')
                        ),
                    ],
                    width=8,
                        ),
                dbc.Col(
                    [
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.P(
                            dcc.Markdown('''
                             Live once a day updates with regards to Ukraine vs Russia, for more details contact [ioteverythin.com](https://www.ioteverythin.com/), last updated at 14:00 GMT on 11-Mar-22
                            ''')
                        ),
                    ],
                    width=5,
                ),
             

            ], 
            justify="center",
            className="mt-5 mb-2",
        ),
    ],
    fluid=True,
)


# top left bar graph 
@app.callback(Output("bar-col", "children"), Input("bar-data", "value"))
def create_bar_graph(data_column):
    bar_grpah = dcc.Graph(
        figure=px.bar(
            dfc, x=data_column, y="Impacted Region", hover_data=["Activity Date"]
        ).update_xaxes(categoryorder="total descending")
    )
    return bar_grpah


# top right map 
@app.callback(Output("map-conslt-col", "children"), Input("map1-conslt-data", "value"))
def create_map(data_column):
    map1 = dcc.Graph(
        config={"displayModeBar": False},
        figure=px.scatter_mapbox(
            dfc_gpd,
            lat="Latitude",
            lon="Longitude",
            size="Length minutes",
            hover_data={"Activity": True, "Longitude": False, "Latitude": False},
            size_max=40,
            color=data_column,
            color_continuous_scale=px.colors.sequential.Bluered,
            zoom=6,
        ).update_layout(
            mapbox_style="stamen-terrain", margin={"r": 0, "t": 0, "l": 0, "b": 0}
        ),
    )

    return map1

if __name__ == "__main__":
    app.run_server(debug=True)
