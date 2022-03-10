from dash import Dash, html, dcc, Input, Output, callback  
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  

dfc = pd.read_csv("Uk5.csv")
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
                                #{"label": "Loss of City", 
                                #"value": "Substance use"},
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
                                    * Russia's bombing of maternity and children's hospital an 'atrocity,' Zelensky says - CNN
                                    * Description:
                                    > Russian forces bombed a maternity and children's hospital in southern Ukraine, authorities there said Wednesday, an attack described by the country's President Volodymyr Zelensky as an "atrocity."
                                    > Read full article:
                                    https://www.cnn.com/2022/03/09/europe/russia-invasion-ukraine-evacuations-03-09-intl/index.html
                                    * U.S. House approves Ukraine aid, Russia oil ban, funds averting U.S. gov't shutdown - Reuters.com
                                    * Description:
                                    > The U.S. House of Representatives on Wednesday voted to rush $13.6 billion in aid to Ukraine as it battles invading Russian forces, along with $1.5 trillion to keep U.S. government programs operating through Sept. 30 and avoid agency shutdowns this weekend.
                                    > Read full article:
                                    https://www.reuters.com/world/us/us-congress-reaches-govt-spending-deal-including-136-bln-ukraine-2022-03-09/
                                    * 'Forgive me that I couldn’t defend you': Dad of slain Ukraine family learned of deaths on Twitter - New York Post 
                                    * Description:
                                    > Serhiy Perebyinis, 43, was in eastern Ukraine tending to his ailing mother when his family was killed. He broke down in tears talking about the senseless killings during an interview.
                                    > Read full article:
                                    https://nypost.com/2022/03/09/dad-of-slain-ukraine-family-learned-of-their-deaths-on-twitter/
                                    * Why the US rejected Poland's plan to send fighter jets to Ukraine - CNN
                                    * Description:
                                    > The Pentagon said Wednesday that it is bluntly opposed to a Polish plan to provide fighter jets to Ukraine.
                                    > Read full article:
                                    https://www.cnn.com/2022/03/09/politics/ukraine-russia-poland-fighter-jets/index.html
                                    * Russia, Belarus squarely in 'default territory' on billions in debt -World Bank - Reuters.com
                                    * Description:
                                    > Russia and Belarus are edging close to default given the massive sanctions imposed against their economies by the United States and its allies over the war in Ukraine, the World Bank's chief economist, Carmen Reinhart, told Reuters.
                                    > Read full article:
                                    https://www.reuters.com/markets/europe/russia-belarus-squarely-default-territory-billions-debt-world-bank-2022-03-09/
                                    * U.S. dismisses Russian claims of biowarfare labs in Ukraine - Reuters
                                    * Description:
                                    > The United States on Wednesday denied renewed Russian accusations that Washington was operating biowarfare labs in Ukraine, calling the claims "laughable" and suggesting Moscow may be laying the groundwork to use a chemical or biological weapon.
                                    > Read full article:
                                    https://www.reuters.com/world/russia-demands-us-explain-biological-programme-ukraine-2022-03-09/
                                    * Russia's Lavrov arrives in Turkey for talks with Ukraine counterpart - Reuters.com
                                    * Description:
                                    > Russia's foreign minister Sergei Lavrov arrived after a flight to Turkey's southern city of Antalya on Wednesday, according to a Reuters witness, ahead of planned talks Thursday with his Ukrainian counterpart Dmytro Kuleba.
                                    > Read full article:
                                    https://www.reuters.com/world/middle-east/russias-lavrov-arrives-turkey-talks-with-ukraine-counterpart-2022-03-09/
                                    * Ukraine war: UK Home Office is in crisis mode over visas - BBC.com
                                    * Description:
                                    > The department is trying to convince an increasingly sceptical nation it has control of the situation.
                                    > Read full article:
                                    https://www.bbc.com/news/uk-60682454
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
