from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from parsing import Parser
import pickle
import numpy as np
import shap
import matplotlib.pyplot as plt
import psycopg2
import pickle
import pandas as pd

app = FastAPI()

# Mount the "static" directory as a static file directory
app.mount("/web", StaticFiles(directory="web"), name="web")

templates = Jinja2Templates(directory="web")  

@app.get("/", response_class=HTMLResponse)
async def read_root():
    
    with open("web/index.html", "r") as file:
        html_content = file.read()
    
    return HTMLResponse(content=html_content)

@app.post("/predict", response_class=HTMLResponse)
async def submit_form(request: Request, hltv_link: str = Form(...), ai_model: str = Form(...), map: str = Form(...)):   
    
    # parser = Parser()
    # parser.start_driver()

    # team_names, team_rating, ranking, matches_winstreak, h2h, weeks, age, _4v5, _5v4, pistol, rounds_lost, rounds_won, first_pick, first_pick_pc, rating_3m, rating_event, winrate, maps_played = parser.inference(hltv_link)
    # if map == 'Mirage':
    #     data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[0:1] + winrate[1:2] + _5v4[0:1] + _5v4[7:8] + _4v5[0:1] + _4v5[7:8]  \
    #         + maps_played[0:1] + maps_played[7:8] + pistol[0:1] + pistol[7:8] + rounds_lost[0:1] + rounds_won[0:1] + first_pick[0:1] + first_pick_pc[0:1]  \
    #         + rounds_lost[7:8] + rounds_won[7:8] + first_pick[1:2] + first_pick_pc[1:2] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    # elif map == 'Inferno':
    #     data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[2:3] + winrate[3:4] + _5v4[1:2] + _5v4[8:9] + _4v5[1:2] + _4v5[8:9]  \
    #         + maps_played[1:2] + maps_played[8:9] + pistol[1:2] + pistol[8:9] + rounds_lost[1:2] + rounds_won[1:2] + first_pick[2:3] + first_pick_pc[2:3]  \
    #         + rounds_lost[8:9] + rounds_won[8:9] + first_pick[3:4] + first_pick_pc[3:4] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    # elif map == 'Nuke':
    #     data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[4:5] + winrate[5:6] + _5v4[2:3] + _5v4[9:10] + _4v5[2:3] + _4v5[9:10]  \
    #         + maps_played[2:3] + maps_played[9:10] + pistol[2:3] + pistol[9:10] + rounds_lost[2:3] + rounds_won[2:3] + first_pick[4:5] + first_pick_pc[4:5]  \
    #         + rounds_lost[9:10] + rounds_won[9:10] + first_pick[5:6] + first_pick_pc[5:6] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    # elif map == 'Overpass':
    #     data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[6:7] + winrate[7:8] + _5v4[3:4] + _5v4[10:11] + _4v5[3:4] + _4v5[10:11]  \
    #         + maps_played[3:4] + maps_played[10:11] + pistol[3:4] + pistol[10:11] + rounds_lost[3:4] + rounds_won[3:4] + first_pick[6:7] + first_pick_pc[6:7]  \
    #         + rounds_lost[10:11] + rounds_won[10:11] + first_pick[7:8] + first_pick_pc[7:8] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    # elif map == 'Vertigo':
    #     data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[8:9] + winrate[9:10] + _5v4[4:5] + _5v4[11:12] + _4v5[4:5] + _4v5[11:12]  \
    #         + maps_played[4:5] + maps_played[11:12] + pistol[4:5] + pistol[11:12] + rounds_lost[4:5] + rounds_won[4:5] + first_pick[8:9] + first_pick_pc[8:9]  \
    #         + rounds_lost[11:12] + rounds_won[11:12] + first_pick[9:10] + first_pick_pc[9:10] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    # elif map == 'Ancient':
    #     data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[10:11] + winrate[11:12] + _5v4[5:6] + _5v4[12:13] + _4v5[5:6] + _4v5[12:13]  \
    #         + maps_played[5:6] + maps_played[12:13] + pistol[5:6] + pistol[12:13] + rounds_lost[5:6] + rounds_won[5:6] + first_pick[10:11] + first_pick_pc[10:11]  \
    #         + rounds_lost[12:13] + rounds_won[12:13] + first_pick[11:12] + first_pick_pc[11:12] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    # elif map == 'Anubus':
    #     data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[12:13] + winrate[13:14] + _5v4[6:7] + _5v4[13:14] + _4v5[6:7] + _4v5[13:14]  \
    #         + maps_played[6:7] + maps_played[13:14] + pistol[6:7] + pistol[13:14] + rounds_lost[6:7] + rounds_won[6:7] + first_pick[12:13] + first_pick_pc[12:13]  \
    #         + rounds_lost[13:14] + rounds_won[13:14] + first_pick[13:14] + first_pick_pc[13:14] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    
    conn = psycopg2.connect(host="localhost", dbname='cs', user='postgres', password='123456', port=5432)
    cur = conn.cursor()

    query = f"""
        SELECT *
        FROM inference
        WHERE inference.link = '{hltv_link}'
        """
    cur.execute(query)

    fetch = list(cur.fetchall()[0])

    if map == 'Mirage':
        data = [fetch[7], fetch[8], fetch[9], fetch[10], fetch[5], fetch[6], fetch[11], fetch[12], fetch[13], fetch[14], fetch[15], fetch[16],
                fetch[23], fetch[86], fetch[25], fetch[88], fetch[26], fetch[89], fetch[24], fetch[87], fetch[27], fetch[90],
                fetch[19], fetch[20], fetch[21], fetch[22], fetch[82],fetch[83], fetch[84], fetch[85], fetch[3], fetch[17], fetch[4], fetch[18]]
    elif map == 'Inferno':
        data = [fetch[7], fetch[8], fetch[9], fetch[10], fetch[5], fetch[6], fetch[11], fetch[12], fetch[13], fetch[14], fetch[15], fetch[16],
                fetch[23+9], fetch[86+9], fetch[25+9], fetch[88+9], fetch[26+9], fetch[89+9], fetch[24+9], fetch[87+9], fetch[27+9], fetch[90+9],
                fetch[19+9], fetch[20+9], fetch[21+9], fetch[22+9], fetch[82+9],fetch[83+9], fetch[84+9], fetch[85+9], fetch[3], fetch[17], fetch[4], fetch[18]]
    elif map == 'Nuke':
        data = [fetch[7], fetch[8], fetch[9], fetch[10], fetch[5], fetch[6], fetch[11], fetch[12], fetch[13], fetch[14], fetch[15], fetch[16],
                fetch[23+18], fetch[86+18], fetch[25+18], fetch[88+18], fetch[26+18], fetch[89+18], fetch[24+18], fetch[87+18], fetch[27+18], fetch[90+18],
                fetch[19+18], fetch[20+18], fetch[21+18], fetch[22+18], fetch[82+18],fetch[83+18], fetch[84+18], fetch[85+18], fetch[3], fetch[17], fetch[4], fetch[18]]
    elif map == 'Overpass':
        data = [fetch[7], fetch[8], fetch[9], fetch[10], fetch[5], fetch[6], fetch[11], fetch[12], fetch[13], fetch[14], fetch[15], fetch[16],
                fetch[23+27], fetch[86+27], fetch[25+27], fetch[88+27], fetch[26+27], fetch[89+27], fetch[24+27], fetch[87+27], fetch[27+27], fetch[90+27],
                fetch[19+27], fetch[20+27], fetch[21+27], fetch[22+27], fetch[82+27],fetch[83+27], fetch[84+27], fetch[85+27], fetch[3], fetch[17], fetch[4], fetch[18]]
    elif map == 'Vertigo':
        data = [fetch[7], fetch[8], fetch[9], fetch[10], fetch[5], fetch[6], fetch[11], fetch[12], fetch[13], fetch[14], fetch[15], fetch[16],
                fetch[23+36], fetch[86+36], fetch[25+36], fetch[88+36], fetch[26+36], fetch[89+36], fetch[24+36], fetch[87+36], fetch[27+36], fetch[90+36],
                fetch[19+36], fetch[20+36], fetch[21+36], fetch[22+36], fetch[82+36],fetch[83+36], fetch[84+36], fetch[85+36], fetch[3], fetch[17], fetch[4], fetch[18]]
    elif map == 'Ancient':
        data = [fetch[7], fetch[8], fetch[9], fetch[10], fetch[5], fetch[6], fetch[11], fetch[12], fetch[13], fetch[14], fetch[15], fetch[16],
                fetch[23+45], fetch[86+45], fetch[25+45], fetch[88+45], fetch[26+45], fetch[89+45], fetch[24+45], fetch[87+45], fetch[27+45], fetch[90+45],
                fetch[19+45], fetch[20+45], fetch[21+45], fetch[22+45], fetch[82+45],fetch[83+45], fetch[84+45], fetch[85+45], fetch[3], fetch[17], fetch[4], fetch[18]]
    elif map == 'Anubis':
        data = [fetch[7], fetch[8], fetch[9], fetch[10], fetch[5], fetch[6], fetch[11], fetch[12], fetch[13], fetch[14], fetch[15], fetch[16],
                fetch[23+54], fetch[86+54], fetch[25+54], fetch[88+54], fetch[26+54], fetch[89+54], fetch[24+54], fetch[87+54], fetch[27+54], fetch[90+54],
                fetch[19+54], fetch[20+54], fetch[21+54], fetch[22+54], fetch[82+54],fetch[83+54], fetch[84+54], fetch[85+54], fetch[3], fetch[17], fetch[4], fetch[18]]

    for index in range(0, 22, 2):
        dif = data[index] - data[index + 1]
        data.append(dif)
    for index in [22,23,25]:
        dif = data[index] - data[index + 4]
        data.append(dif)
    for index in range(30,32):
        dif = data[index] - data[index + 2]
        data.append(dif)
    
    if ai_model == 'XGBoost':
        with open('models/xgb.pkl', 'rb') as file:
            model = pickle.load(file)
        explainer = shap.Explainer(model)
    elif ai_model == 'CatBoost':
        with open('models/cb.pkl', 'rb') as file:
            model = pickle.load(file)
        explainer = shap.Explainer(model)
    elif ai_model == 'LightGBM':
        with open('models/lgb.pkl', 'rb') as file:
            model = pickle.load(file)
        explainer = shap.Explainer(model)
    elif ai_model == 'LogReg':
        with open('models/logReg.pkl', 'rb') as file:
            model = pickle.load(file)
        train = pd.read_csv(r"C:\Users\turek_hd7cu13\coding\cs_bot\train_data.csv")
        explainer = shap.KernelExplainer(model.predict, data=train[:100])
    elif ai_model == 'LDA':
        with open('models/LDA.pkl', 'rb') as file:
            model = pickle.load(file)
        train = pd.read_csv(r"C:\Users\turek_hd7cu13\coding\cs_bot\train_data.csv")
        explainer = shap.KernelExplainer(model.predict, data=train[:100])
    # print(model)

    np_data = np.array(data).reshape(1,-1)

    with open('cs_pipeline.pkl','rb') as f:
        pipeline = pickle.load(f)

    df = pd.DataFrame(np_data, columns=["t1_winstreak","t2_winstreak","t1_h2h","t2_h2h",
                            "t1_ranking","t2_ranking","t1_weeks","t2_weeks","t1_age","t2_age","t1_rating","t2_rating",
                            "t1_winrate","t2_winrate","t1_5v4","t2_5v4","t1_4v5","t2_4v5","t1_maps","t2_maps",  
                            "t1_pistol","t2_pistol","t1_rounds_lost", "t1_rounds_won", "t1_fp", "t1_fp_percent",
                            "t2_rounds_lost", "t2_rounds_won", "t2_fp", "t2_fp_percent","t1_team_rating","t1_event_rating",
                            "t2_team_rating","t2_event_rating", "winstreak_diff", "h2h_diff", "ranking_diff", "weeks_diff",
                            "age_diff",	"rating_diff", "winrate_diff", "5v4_diff", "4v5_diff", "maps_diff",	"pistol_diff",
                            "rounds_lost_diff", "rounds_won_diff", "fp_percent_diff", "team_rating_diff", "event_rating_diff"])
    cols_to_scale = [col for col in df.columns if col != 't1_fp' and col != 't2_fp']
    df.loc[:, cols_to_scale] = pipeline.transform(df.loc[:, cols_to_scale])
    pred = model.predict(df)   
    shap_values = explainer.shap_values(df)

    # print(pred)
    # print(shap_values[0][0])
    # print(shap_values.values[0,:,1]
    shap.plots.waterfall(explainer(df)[0,:,1])

    if ai_model == 'LightGBM':
        if pred[0] == 0:
            shap_values = shap_values[0][0]
            sort = sorted(zip(shap_values, np.linspace(0,49, dtype=np.int32)), key=lambda x: x[0], reverse=False)
        else:
            shap_values = shap_values[1][0]
            sort = sorted(zip(shap_values, np.linspace(0,49, dtype=np.int32)), key=lambda x: x[0], reverse=True)
    else:
        if (pred[0] == 0 and type(pred[0]) is not str) or (pred[0] == 'False' and type(pred[0]) is str):
            sort = sorted(zip(shap_values[0], np.linspace(0,49, dtype=np.int32)), key=lambda x: x[0], reverse=False)
        else:
            sort = sorted(zip(shap_values[0], np.linspace(0,49, dtype=np.int32)), key=lambda x: x[0], reverse=True)

    sort = list(sort)
    # print(sort)
    f_names = ["t1_winstreak","t2_winstreak","t1_h2h","t2_h2h","t1_ranking","t2_ranking","t1_weeks","t2_weeks","t1_age","t2_age","t1_rating","t2_rating","t1_winrate","t2_winrate","t1_5v4","t2_5v4","t1_4v5","t2_4v5","t1_maps","t2_maps","t1_pistol","t2_pistol","t1_rounds_lost","t1_rounds_won","t1_fp","t1_fp_percent","t2_rounds_lost","t2_rounds_won","t2_fp","t2_fp_percent","t1_team_rating","t1_event_rating","t2_team_rating","t2_event_rating","winstreak_diff","h2h_diff","ranking_diff","weeks_diff","age_diff","rating_diff","winrate_diff","5v4_diff","4v5_diff","maps_diff","pistol_diff","rounds_lost_diff","rounds_won_diff","fp_percent_diff","team_rating_diff","event_rating_diff"]

    if (pred[0] == 0 and type(pred[0]) is not str) or (pred[0] == 'False' and type(pred[0]) is str):
        out = f"Given the stats of both teams and their performance on map {map}, {fetch[2]} is more likely to win"
    else:
        out = f"Given the stats of both teams and their performance on map {map}, {fetch[1]} is more likely to win"
    # shap.plots.bar(shap_values)
    # plt.savefig("shap_summary_plot.png")

    # 'hltv_link' contains the submitted link
    with open("web/pred.html", "r") as file:
        html_content = file.read()
    
    rounded_array = np.round(np_data, 2)
    return templates.TemplateResponse("pred.html", {"request": request, "result": out, "stat1": str(rounded_array[0,0]),
                                                    "Important1": f_names[sort[0][1]], "Important2": f_names[sort[1][1]],
                                                    "Important3": f_names[sort[2][1]], "Important4": f_names[sort[3][1]],
                                                    "Important5": f_names[sort[4][1]],
                                                    "Team1": fetch[1], "Team2": fetch[2],
                                                    "stat2": str(rounded_array[0,1]), "stat3": str(rounded_array[0,2]), "stat4": str(rounded_array[0,3]),
                                                    "stat5": str(rounded_array[0,4]), "stat6": str(rounded_array[0,5]), "stat7": str(rounded_array[0,6]),
                                                    "stat8": str(rounded_array[0,7]), "stat9": str(rounded_array[0,8]), "stat10": str(rounded_array[0,9]),
                                                    "stat11": str(rounded_array[0,10]), "stat12": str(rounded_array[0,11]), "stat13": str(rounded_array[0,12]),
                                                    "stat14": str(rounded_array[0,13]), "stat15": str(rounded_array[0,14]), "stat16": str(rounded_array[0,15]),
                                                    "stat17": str(rounded_array[0,16]), "stat18": str(rounded_array[0,17]), "stat19": str(rounded_array[0,18]),
                                                    "stat20": str(rounded_array[0,19]), "stat21": str(rounded_array[0,20]), "stat22": str(rounded_array[0,21]),
                                                    "stat23": str(rounded_array[0,22]), "stat24": str(rounded_array[0,26]), "stat25": str(rounded_array[0,23]),
                                                    "stat26": str(rounded_array[0,27]), "stat27": str(rounded_array[0,24]), "stat28": str(rounded_array[0,28]),
                                                    "stat29": str(rounded_array[0,25]), "stat30": str(rounded_array[0,29]), "stat31": str(rounded_array[0,30]),
                                                    "stat32": str(rounded_array[0,32]), "stat33": str(rounded_array[0,31]), "stat34": str(rounded_array[0,33])})
    # # return {"hltv_link": hltv_link, "Model": ai_model, "Map": map, "Predict": pred}