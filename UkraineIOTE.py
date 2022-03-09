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
                                    * Russia invades Ukraine: Live updates - CNN
                                    * Description:
                                    > US President Joe Biden announced a ban on Russian energy imports to the US as Ukraine's President urged the UK Parliament to strengthen sanctions against Moscow and vowed the country will "fight to the end." Follow here for live news. updates from on the grou…
                                    > Read full article:
                                    https://www.cnn.com/europe/live-news/ukraine-russia-putin-news-03-09-22/index.html
                                    * Attacks hits Ukraine children's hospital, officials say - The Associated Press - en Español
                                    * Description:
                                    > KYIV, Ukraine (AP) — A Russian attack severely damaged a maternity hospital in the besieged port city of Mariupol, Ukraine said Wednesday, and citizens trying to escape shelling on the outskirts of Kyiv streamed toward the capital amid warnings from the West …
                                    > Read full article:
                                    https://apnews.com/article/russia-ukraine-kyiv-europe-2bed71c00916d44ea951c5809b446db3
                                    * Ukraine warns of risk of radiation leak at occupied Chernobyl nuclear plant - Reuters UK
                                    * Description:
                                    > Ukraine appealed to Russia for a temporary ceasefire on Wednesday to allow repairs to be made to a power line to the Chernobyl nuclear power plant, warning that there could be a radiation leak if the electricity outage continued.
                                    > Read full article:
                                    https://www.reuters.com/world/ukraine-nuclear-firm-warns-radiation-risk-after-power-cut-occupied-chernobyl-2022-03-09/
                                    * War in Ukraine: McDonald’s, Coca-Cola and Starbucks halt Russian sales - BBC.com
                                    * Description:
                                    > Western companies are turning their backs on Russia amid sanctions and violence in Ukraine.
                                    > Read full article:
                                    https://www.bbc.com/news/business-60665877
                                    * MBS rejected Biden request to talk Russia, Ukraine oil crisis: WSJ - Business Insider
                                    * Description:
                                    > The US needs new suppliers after banning Russian energy imports. Mohammed bin Salman has spoken harshly about the US after Biden ostracized him.
                                    > Read full article:
                                    https://www.businessinsider.com/saudi-mbs-rejected-biden-request-discuss-russia-oil-crisis-wsj-2022-3
                                    * Top lawmakers reach deal on Ukraine aid, $1.5T spending - The Associated Press - en Español
                                    * Description:
                                    > WASHINGTON (AP) — Congressional leaders reached a bipartisan deal early Wednesday providing $13.6 billion to help Ukraine and European allies plus billions more to battle the pandemic as part of an overdue $1.5 trillion measure financing federal agencies for …
                                    > Read full article:
                                    https://apnews.com/article/russia-ukraine-biden-covid-health-business-fa702b0f9efa4805b622739d302bc4cf
                                    * Foreign volunteers get Ukrainian citizenship in fight against Russia, Ukraine says - Fox News
                                    * Description:
                                    > Foreign volunteers who join Ukrainian forces in the fight against Russia will be granted citizenship by the Ukrainian government if they want, a Ukrainian government official said.
                                    > Read full article:
                                    https://www.foxnews.com/world/foreign-volunteers-ukrainian-citizenship-fight-russia-govt
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
