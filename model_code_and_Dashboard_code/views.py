import os
import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_gif_component as Gif
import dash_table
import pandas as pd
import json


from model_code_and_Dashboard_code.train import load_clf

train_PATH=os.path.dirname(os.path.abspath(__file__))

train_df = pd.read_csv(os.path.join(train_PATH, os.path.join("data", "columns.csv")),index_col=False)

table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",

}

global classifer

classifer=load_clf()



app = dash.Dash(__name__)

app.layout = html.Div(
    className="",
    children=[
        html.Div(className="pkcalc-banner",
                 children=[
                    html.H2("Human Activity Recognition Dashboard", style={"text-align": "left", "color": "white"}),
                    html.A(id="gh-link",
                           children=["View on GitHub"],
                           href="https://github.com/yasmenamr/Human_Activity_Recognition_Dashboard",
                           style={"color": "white", "border": "solid 2px white"},
                    ),
                    html.Img(src=app.get_asset_url("GitHub-Mark-Light-64px.png")),
                ]
        ),
        html.H4('The Human Activity Recognition machine learning model was built from the recordings from smartphones with embedded inertial sensors.'
                ,style={'margin-top': '10rem','margin-bottom': '0rem',
                        "text-align": "left",'padding':0,'margin-left': '6rem',}
        ),
        html.Hr(style={'margin-top': '0rem','padding':"0px"}),
        html.Div(style={'padding':"0pxl"},
                 className="container",
                 children=[html.H6('If you want to recognize your activity please insert your recordings:',style={"text-align": "left",'padding':0}),
                           html.Div(className="twelve columns pkcalc-data-table",
                                    children=[dash_table.DataTable(
                                    id="data-table",
                                    columns=[{"name": i, "id": i} for i in train_df.columns],
                                    data=train_df.to_dict('records')[:1],
                                    editable=True,
                                    style_header=table_header_style,style_cell={ 'font-size': '120%',},
                                    active_cell={"row": 1},
                                    selected_cells=[{"row": 0, "column": 0}],
                                             )
                                    ],
                           ),
                           html.Button(id='submit-button', n_clicks=0, children='Submit', type="submit",
                                       style={'color': "white",
                                              'backgroundColor': "rgb(2,21,70)",
                                              "width": "100%"
                                       },

                           ),
                ],
        ),


        html.Div(className="container",
                 children=[html.H2(id='output-activity',
                                   style={"text-align": "center", "width": "100%"}
                                   ),

                            html.Div(id='out',
                                     style={"text-align": "center", "width": "100%"}
                            )
                 ]
        )


    ],style={"text-align": "center"}
)


# ------------------------------- CALLBACKS ---------------------------------------- #



@app.callback(Output('output-activity', 'children'),
                   [Input("submit-button", "n_clicks")], [State("data-table", "data")])
def get_activity(n_clicks, data):
    data = list(json.loads(json.dumps(data[0])).values())

    data=[x for x in data if pd.notnull(x)]

    if not data:
        return None


    if len(data) == 562:
        data=data[:-1]
    else:
        return html.H3('the length of data must be 562')


    data=[data]
    s=classifer.predict(data)

    return 'You are ',s[0]



@app.callback(Output('out', 'children'),
                   [Input("submit-button", "n_clicks")], [State("data-table", "data")])
def get_gif(n_clicks, data):

    data=list(json.loads(json.dumps(data[0])).values())
    data = [x for x in data if pd.notnull(x)]
    if not data:
        return html.H3("Your activity will appear here")
    if len(data) == 562:
        data = data[:-1]

    else:
        return html.H3('Please, make sure that all blank cells contain data')

    data = [data]
    s = classifer.predict(data)
    if s == ['LAYING']:
        gif='https://media.tenor.com/images/2d010e4d537648a8af03b006e6a3fdd9/tenor.gif'
        still = app.get_asset_url("laying.png"),

    elif s==['SITTING']:
        gif='https://i.pinimg.com/originals/f4/c3/da/f4c3da24fac962cee926c4595ce46923.gif'
        still = app.get_asset_url("sitting.png"),

    elif s==['STANDING']:
        gif='https://i.pinimg.com/originals/fb/69/b0/fb69b0b94fd3e40bf041be3db4b8b5e9.gif'
        still = app.get_asset_url("standing.png"),

    elif s==['WALKING']:
        gif='http://blogs.studentlife.utoronto.ca/lifeatuoft/files/2018/11/72f02440701089.57894e458a58b.gif'
        still=app.get_asset_url("walking .png"),

    elif s==['WALKING_DOWNSTAIRS']:
        gif='https://thumbs.gfycat.com/FondFlusteredIvorybilledwoodpecker-size_restricted.gif'
        still = app.get_asset_url("wds.png"),

    elif s==['WALKING_UPSTAIRS']:
        gif='https://cdn2.scratch.mit.edu/get_image/gallery/5658656_170x100.png'
        still=app.get_asset_url("wus.png"),

    return html.Div([
        Gif.GifPlayer(
            gif=gif,
            still=still[0],
            autoplay=True,
        ),
        ])

# try this data the user is walking:
#0.31263404,-0.026367749,-0.13095121,-0.3530986,-0.01738215,-0.1278076,-0.39527374,-0.0543888,-0.095763059,-0.29039716,-0.14554645,-0.19315657,0.28053625,-0.02305703,0.39875442,-0.14859591,-0.7891772,-0.81300152,-0.65669769,-0.46625697,-0.35449084,-0.076900473,0.36336909,0.38204084,0.018222124,-0.35435942,0.1954133,0.18395289,-0.11210916,-0.25797663,0.3126983,-0.060445461,0.15767416,-0.37885352,0.28878928,-0.065076673,-0.19578783,-0.20380286,-0.033051808,0.34722497,0.94691727,-0.26205559,-0.020235796,-0.9850642,-0.94652431,-0.83709377,-0.98656429,-0.95768667,-0.84192698,0.87654171,-0.27383035,0.008912625,0.95787983,-0.2653281,-0.066073,-0.29318366,0.85618709,-0.88497202,-0.99749767,-0.99028678,-0.98088501,-0.84757716,-1,-1,-0.69833923,-0.4923716,0.5678772,-0.64258496,0.71645958,-0.23299274,0.24871294,-0.31873091,0.40964336,-0.68734168,0.69941204,-0.71089176,0.71883643,0.71172858,0.72725057,0.64532281,-0.094394668,0.013017354,-0.30579489,-0.30650885,-0.068948743,-0.60594792,-0.26180846,-0.082266065,-0.57439078,-0.62345012,-0.43528672,-0.81424129,0.16433001,0.085692605,0.43725651,-0.28019975,-0.75679758,-0.56177796,-0.9175564,-0.19670481,-0.33095367,-0.50899884,0.72431662,0.65090847,0.41613865,-0.32362457,0.071082293,0.30701579,-0.079226997,-0.41271868,0.37745559,-0.075324418,0.38717181,-0.32428058,0.14067928,0.061217451,-0.23726395,-0.28267794,-0.20707937,0.6667628,-0.23928593,0.078229978,0.043137262,-0.46501506,-0.16740045,-0.43151087,-0.47543749,-0.18577029,-0.46468858,-0.52838613,-0.47587563,-0.22219519,0.29240461,0.58087297,0.40165487,-0.2150521,-0.8405364,-0.65388669,-0.84885148,-0.45336831,-0.28017638,-0.63061242,-0.13880155,0.062191497,0.2426176,-0.46238695,0.25938451,0.42517769,-0.56765759,-0.4571042,0.46300897,-0.41819257,0.33756148,-0.32626704,0.39798666,-0.53689937,0.66487723,-0.1451654,0.082040898,0.04536196,0.034467284,-0.34622965,0.19077019,-0.28902666,-0.49804596,-0.54948827,-0.32184491,-0.52086368,-0.54105951,-0.26182559,-0.48085665,-0.58398099,0.31267113,0.53601577,0.64569391,-0.46891359,-0.74533756,-0.87297068,-0.8963348,-0.45450534,-0.54969046,-0.50555029,0.64361994,0.53646469,0.67613516,-0.22475144,0.026941594,0.31824947,0.3253255,-0.44443,0.46098498,-0.1724978,0.066385308,-0.43546963,0.47694341,-0.46065794,0.1335937,0.58433164,-0.23487023,-0.1435431,-0.1696296,-0.32073899,-0.37802238,-0.27682438,-0.63558527,-0.1696296,-0.64912028,-0.43840012,0.76189413,-0.09730924,0.025193085,0.031041608,0.043228105,-0.1696296,-0.32073899,-0.37802238,-0.27682438,-0.63558527,-0.1696296,-0.64912028,-0.43840012,0.76189413,-0.09730924,0.025193085,0.031041608,0.043228105,-0.28756092,-0.27400211,-0.33155011,-0.27509806,-0.34326231,-0.28756092,-0.73131457,-0.41583906,0.69045091,0.0087500811,0.00012225291,-0.20179033,0.14501513,-0.21472204,-0.22792935,-0.1170125,-0.39781524,-0.49210335,-0.21472204,-0.65980214,-0.10040395,0.52797983,-0.0015879448,-0.028831011,0.038606806,-0.080189392,-0.46434627,-0.46330737,-0.51363782,-0.43962213,-0.5148462,-0.46434627,-0.84919701,-0.58625354,0.92942022,-0.064977194,0.27908648,-0.35397063,-0.1760246,-0.2749068,-0.062349562,-0.31909457,-0.38657078,-0.055909878,-0.098385402,-0.26088506,-0.076015023,-0.18608503,-0.56052893,-0.35368948,-0.065185822,-0.39830449,-0.92102018,-0.9015767,-0.11471639,-0.78887397,-0.51220934,-0.61148715,-0.27728118,-0.36804635,-0.5927095,0.52973064,0.53066422,0.38178857,-0.80645161,-0.33333333,-0.92307692,-0.2490708,0.0013439574,-0.22652212,-0.33774508,-0.75527568,-0.35502774,-0.73418465,-0.078237573,-0.3807269,-0.83698894,-0.73595801,-0.7608114,-0.76003308,-0.92449311,-0.81587839,-0.91539137,-0.91998812,-0.79210545,-0.72313073,-0.88379257,-0.91693209,-0.78988274,-0.77281224,-0.73454903,-0.4448388,-0.80590483,-0.7495052,-0.78908683,-0.87929882,-0.88543084,-0.99827458,-0.51100842,-0.74004991,-0.79954584,-0.92933411,-0.51888439,-0.75233785,-0.57985646,-0.85011646,-0.90314141,-0.96389603,-0.97855038,-0.93386792,-0.90620804,-0.88184095,-0.6158334,-0.92518227,-0.96545106,-0.89811278,-0.60944428,-0.96435592,-0.32488554,-0.15821185,-0.56272771,-0.34905958,-0.032820151,-0.64777257,-0.18434277,-0.11187479,-0.58908177,-0.41965993,-0.10802593,-0.75145508,-0.66103403,-0.77265762,-0.88328737,-0.23957588,-0.75642179,-0.56179922,-0.91768109,-0.1466556,-0.35882734,-0.52591886,0.5718566,0.59295317,0.27205558,-0.52,-0.6,-0.44,-0.33298679,-0.40132381,-0.41857923,-0.23851322,-0.66540428,-0.089528226,-0.59627009,-0.63250551,-0.94594187,-0.86466437,-0.74419145,-0.80085618,-0.81639774,-0.95332705,-0.82029093,-0.92679153,-0.9606993,-0.7755424,-0.76122553,-0.89470092,-0.92046134,-0.74403272,-0.79370222,-0.81417329,-0.48107316,-0.75543911,-0.73249337,-0.80250887,-0.84681634,-0.86365988,-0.99037633,-0.48564719,-0.69542815,-0.77396141,-0.87964933,-0.51818976,-0.74492661,-0.85395772,-0.87008391,-0.92499446,-0.95230487,-0.97473512,-0.94052159,-0.94395609,-0.99074206,-0.83701608,-0.93837591,-0.96270933,-0.94576202,-0.87637697,-0.95641798,-0.3276796,-0.25778599,-0.35621853,-0.50858961,-0.12194059,-0.51041089,-0.34949394,-0.3110388,-0.38415107,-0.54302656,-0.15945756,-0.70431485,-0.93344367,-0.45929153,-0.44084397,-0.25882146,-0.85612689,-0.65210351,-0.83656295,-0.33431292,-0.41038051,-0.53771481,0.58744641,0.6506413,0.37390231,-0.33333333,-0.93548387,-0.5862069,-0.070288769,-0.11308313,-0.020525379,-0.34156456,-0.68430793,0.039102635,-0.34325879,-0.4106278,-0.78078179,-0.94176588,-0.43321254,-0.86888381,-0.95088706,-0.96545044,-0.90819682,-0.95806913,-0.95995967,-0.86238693,-0.87450144,-0.93866361,-0.95890568,-0.85759069,-0.94682305,-0.5104158,-0.94897541,-0.92995086,-0.91652543,-0.93088605,-0.92786663,-0.88809341,-0.88008617,-0.63716212,-0.90919988,-0.92956023,-0.86939275,-0.62949457,-0.91414061,-0.86972836,-0.91297461,-0.9564242,-0.95695194,-0.94586849,-0.91229201,-0.89596369,-0.90844162,-0.84691105,-0.93761089,-0.93663218,-0.90138888,-0.84177774,-0.95064905,-0.25871717,-0.46375538,-0.26177004,-0.66204365,-0.91953181,-0.25871717,-0.76474809,-0.39973615,0.44493725,-0.93103448,0.024106987,-0.64231585,-0.88387513,-0.21590346,-0.36040189,-0.24065679,-0.51015315,-0.018009841,-0.21590346,-0.73109646,-0.29374714,0.33628378,-0.9047619,0.015740678,-0.36629719,-0.73687222,-0.30917911,-0.30476058,-0.22241719,-0.38038878,-0.8920393,-0.30917911,-0.70031593,-0.22334376,0.64346088,-0.84615385,-0.038943067,-0.34411148,-0.67422888,-0.47289324,-0.48842516,-0.43005295,-0.53567704,-0.40341371,-0.47289324,-0.85476289,-0.40754818,0.48353643,-0.9047619,-0.020913284,-0.20147706,-0.59466014,-0.51615414,0.46159389,0.92173483,-0.36722405,-0.7601763,0.26295137,0.035725938,"1"