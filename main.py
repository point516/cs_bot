from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from parsing import Parser

app = FastAPI()

# Mount the "static" directory as a static file directory
app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # You can use Python's open() function to read the HTML file
    with open("web/index.html", "r") as file:
        html_content = file.read()
    
    return HTMLResponse(content=html_content)

@app.post("/predict")
async def submit_form(hltv_link: str = Form(...), ai_model: str = Form(...), map: str = Form(...)):   
    parser = Parser()
    parser.start_driver()

    team_names, team_rating, ranking, matches_winstreak, h2h, weeks, age, _4v5, _5v4, pistol, rounds_lost, rounds_won, first_pick, first_pick_pc, rating_3m, rating_event, winrate, maps_played = parser.inference(hltv_link)
    if map == 'Mirage':
        data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[0:1] + winrate[1:2] + _5v4[0:1] + _5v4[7:8] + _4v5[0:1] + _4v5[7:8]  \
            + maps_played[0:1] + maps_played[7:8] + pistol[0:1] + pistol[7:8] + rounds_lost[0:1] + rounds_won[0:1] + first_pick[0:1] + first_pick_pc[0:1]  \
            + rounds_lost[7:8] + rounds_won[7:8] + first_pick[1:2] + first_pick_pc[1:2] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    elif map == 'Inferno':
        data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[2:3] + winrate[3:4] + _5v4[1:2] + _5v4[8:9] + _4v5[1:2] + _4v5[8:9]  \
            + maps_played[1:2] + maps_played[8:9] + pistol[1:2] + pistol[8:9] + rounds_lost[1:2] + rounds_won[1:2] + first_pick[2:3] + first_pick_pc[2:3]  \
            + rounds_lost[8:9] + rounds_won[8:9] + first_pick[3:4] + first_pick_pc[3:4] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    elif map == 'Nuke':
        data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[4:5] + winrate[5:6] + _5v4[2:3] + _5v4[9:10] + _4v5[2:3] + _4v5[9:10]  \
            + maps_played[2:3] + maps_played[9:10] + pistol[2:3] + pistol[9:10] + rounds_lost[2:3] + rounds_won[2:3] + first_pick[4:5] + first_pick_pc[4:5]  \
            + rounds_lost[9:10] + rounds_won[9:10] + first_pick[5:6] + first_pick_pc[5:6] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    elif map == 'Overpass':
        data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[6:7] + winrate[7:8] + _5v4[3:4] + _5v4[10:11] + _4v5[3:4] + _4v5[10:11]  \
            + maps_played[3:4] + maps_played[10:11] + pistol[3:4] + pistol[10:11] + rounds_lost[3:4] + rounds_won[3:4] + first_pick[6:7] + first_pick_pc[6:7]  \
            + rounds_lost[10:11] + rounds_won[10:11] + first_pick[7:8] + first_pick_pc[7:8] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    elif map == 'Vertigo':
        data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[8:9] + winrate[9:10] + _5v4[4:5] + _5v4[11:12] + _4v5[4:5] + _4v5[11:12]  \
            + maps_played[4:5] + maps_played[11:12] + pistol[4:5] + pistol[11:12] + rounds_lost[4:5] + rounds_won[4:5] + first_pick[8:9] + first_pick_pc[8:9]  \
            + rounds_lost[11:12] + rounds_won[11:12] + first_pick[9:10] + first_pick_pc[9:10] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    elif map == 'Ancient':
        data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[10:11] + winrate[11:12] + _5v4[5:6] + _5v4[12:13] + _4v5[5:6] + _4v5[12:13]  \
            + maps_played[5:6] + maps_played[12:13] + pistol[5:6] + pistol[12:13] + rounds_lost[5:6] + rounds_won[5:6] + first_pick[10:11] + first_pick_pc[10:11]  \
            + rounds_lost[12:13] + rounds_won[12:13] + first_pick[11:12] + first_pick_pc[11:12] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    elif map == 'Anubus':
        data = matches_winstreak + h2h + ranking + weeks + age + rating_3m + winrate[12:13] + winrate[13:14] + _5v4[6:7] + _5v4[13:14] + _4v5[6:7] + _4v5[13:14]  \
            + maps_played[6:7] + maps_played[13:14] + pistol[6:7] + pistol[13:14] + rounds_lost[6:7] + rounds_won[6:7] + first_pick[12:13] + first_pick_pc[12:13]  \
            + rounds_lost[13:14] + rounds_won[13:14] + first_pick[13:14] + first_pick_pc[13:14] + team_rating[0:1] + rating_event[0:1] + team_rating[1:2] + rating_event[1:2]
    
    for index in range(0, 22, 2):
        dif = data[index] - data[index + 1]
        data.append(dif)
    for index in [22,23,25]:
        dif = data[index] - data[index + 4]
        data.append(dif)
    for index in range(30,32):
        dif = data[index] - data[index + 2]
        data.append(dif)
    
    print(data)
    # 'hltv_link' contains the submitted link
    return {"hltv_link": hltv_link, "Model": ai_model, "Map": map}