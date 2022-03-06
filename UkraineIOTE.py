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
                                    * Russia and Ukraine agree to temporary ceasefire to let civilians leave two Ukraine cities - CNBC
                                    * Description:
                                    > A Ukrainian official tweeted that "humanitarian corridors" were being prepared in Mariupol and Volnovakha.
                                    > Read full article:
                                    https://www.cnbc.com/2022/03/05/russian-state-media-claims-temporary-ceasefire-at-mariupol-volnovakha.html
                                    * "Unless At Gunpoint": Elon Musk On Blocking Russian News On Starlink - NDTV
                                    * Description:
                                    > SpaceX chief Elon Musk said on Saturday that its Starlink satellite broadband service has been told by some governments, not Ukraine, to block Russian news sources.
                                    > Read full article:
                                    https://www.ndtv.com/world-news/elon-musks-says-spacexs-starlink-wont-block-russian-news-sources-unless-on-gunpoint-2804990
                                    * Attack on Ukrainian nuclear plant triggers worldwide alarm - The Associated Press - en Español
                                    * Description:
                                    > KYIV, Ukraine (AP) — Russian troops Friday seized the biggest nuclear power plant in Europe after a middle-of-the-night attack that set it on fire and briefly raised worldwide fears of a catastrophe  in the most chilling turn yet in Moscow's invasion of Ukrai…
                                    > Read full article:
                                    https://apnews.com/article/russia-ukraine-war-nuclear-plant-attack-33b6c1709dee937750f95c6786832840
                                    * Mila Kunis, Ashton Kutcher GoFundMe Campaign To Help Ukraine’s Needy Approaches $10M Mark - Deadline
                                    * Description:
                                    > Mila Kunis hasn’t forgotten where she came from. The actress and husband Ashton Kutcher have launched a fundraiser on the GoFundMe site to provide humanitarian aid to Ukraine. In just one day, the fundraiser has accumulated pledges of $9.3 million. Kutcher an…
                                    > Read full article:
                                    https://deadline.com/2022/03/mila-kunis-ashton-kutcher-gofundme-ukraine-campaign-1234971577/
                                    * Zelensky slams NATO over refusing to implement no-fly zone over Ukraine - The Hill
                                    * Description:
                                    > Ukrainian President Volodymyr Zelensky on Friday slammed NATO as being "weak" and "underconfident...
                                    > Read full article:
                                    https://thehill.com/policy/international/596972-zelensky-slams-nato-over-refusing-to-implement-no-fly-zone-over-ukraine
                                    * Electronic Arts halts all sales in Russia and Belarus - PC Gamer
                                    * Description:
                                    > EA says it will not sell games through Origin, the EA app, or "platform partners" while Russia's invasion of Ukraine continues.
                                    > Read full article:
                                    https://www.pcgamer.com/electronic-arts-halts-all-sales-in-russia-and-belarus/
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
@callback(Output("bar-col", "children"), Input("bar-data", "value"))
def create_bar_graph(data_column):
    bar_grpah = dcc.Graph(
        figure=px.bar(
            dfc, x=data_column, y="Impacted Region", hover_data=["Activity Date"]
        ).update_xaxes(categoryorder="total descending")
    )
    return bar_grpah


# top right map 
@callback(Output("map-conslt-col", "children"), Input("map1-conslt-data", "value"))
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
