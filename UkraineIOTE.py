from dash import Dash, html, dcc, Input, Output, callback  
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  

dfc = pd.read_csv("Ukupdates.csv")
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
       "Fleed",
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
    __name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True
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
                                {"label": "Region", "value": "Program"},
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
                                    "label": "Fleed the Country",
                                    "value": "Fleed",
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
                                    * The Russia-Ukraine War: Latest News and Live Updates - The Wall Street Journal
                                    * Description:
                                    > Full coverage of Russia's invasion of Ukraine, from The Wall Street Journal
                                    > Read full article:
                                    https://www.wsj.com/livecoverage/russia-ukraine-latest-news-2022-03-07
                                    * 'Top of the kill list': Rep. John Garamendi speaks with Ukraine President Volodymyr Zelenskyy - KCRA Sacramento
                                    * Description:
                                    > Garamendi said Ukraine's President emphasized that Russian forces are moving away from targeting the Ukrainian military and are now attacking communities.
                                    > Read full article:
                                    https://www.kcra.com/article/rep-john-garamendi-speaks-ukraine-president-volodymyr-zelenskyy/39337159
                                    * Ukraine Faces Fresh Wave of Attacks Focused on Population Centers - The Wall Street Journal
                                    * Description:
                                    > Civilian casualties mount in Ukraine as Russian shelling, airstrikes intensify ahead of new talks
                                    > Read full article:
                                    https://www.wsj.com/articles/ukraine-resumes-evacuation-attempts-as-russia-presses-offensive-11646564330
                                    * Pope Francis: Ukraine humanitarian crisis 'growing dramatically' amid 'river of blood and tears' - Fox News
                                    * Description:
                                    > Pope Francis condemned the Russia-Ukraine conflict in his strongest language yet during his weekly address in St. Peter's Square at the Vatican on Sunday.
                                    > Read full article:
                                    https://www.foxnews.com/world/pope-francis-ukraine-humanitarian-crisis
                                    * NATO nations have 'green light' to send jets to Ukraine; cease-fire in Mariupol collapses: Live updates - USA TODAY
                                    * Description:
                                    > NATO countries supporting Ukraine against the Russian invasion have a “green light” to send fighter jets as part of their military aid. Latest news.
                                    > Read full article:
                                    https://www.usatoday.com/story/news/politics/2022/03/06/russia-ukraine-invasion-updates/9401259002/
                                    * U.S. gasoline prices soar to highest since 2008 on Russia conflict, AAA says - Reuters
                                    * Description:
                                    > U.S. gasoline prices jumped 11% over the past week to the highest since 2008 as global sanctions cripple Russia's ability to export crude oil after its invasion of Ukraine, automobile club AAA said on Sunday.
                                    > Read full article:
                                    https://www.reuters.com/business/energy/us-gasoline-prices-soar-highest-since-2008-russia-conflict-aaa-2022-03-06/
                                    * ‘Grave concern’ as Ukraine Zaporizhzhia nuclear plant under Russian orders - The Guardian
                                    * Description:
                                    > International Atomic Energy Agency says Russian military orders of staff at nuclear plant violate international safety protocols
                                    > Read full article:
                                    https://amp.theguardian.com/world/2022/mar/06/ukraine-zaporizhzhia-nuclear-plant-staff-under-russian-orders
                                    * For German Firms, Ties to Russia Are Personal, Not Just Financial - The New York Times
                                    * Description:
                                    > The economic fallout from Russia’s invasion of Ukraine is only part of the pain for German companies.
                                    > Read full article:
                                    https://www.nytimes.com/2022/03/06/business/germany-russia-companies.html
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
                             Live once a day updates with regards to Ukraine vs Russia, for more details contact [ioteverythin.com](https://www.ioteverythin.com/)
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
