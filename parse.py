from parsing import Parser
import psycopg2

conn = psycopg2.connect(host="localhost", dbname='cs', user='postgres', password='123456', port=5432)
cur = conn.cursor()

parser = Parser()
parser.start_driver()

matches = ["https://www.hltv.org/matches/2369492/natus-vincere-vs-eternal-fire-iem-katowice-2024"]

for match in matches:    
    team_names, team_rating, ranking, matches_winstreak, h2h, weeks, age, _4v5, _5v4, pistol, rounds_lost, rounds_won, first_pick, first_pick_pc, rating_3m, rating_event, winrate, maps_played = parser.inference(match)
    insert_query = ("""INSERT INTO inference (
                                            link,
                                            t1_name, t2_name, t1_event_team_rating, t2_event_team_rating,
                                            t1_ranking, t2_ranking, t1_winstreak, t2_winstreak, t1_h2h,
                                            t2_h2h, t1_weeks, t2_weeks, t1_age, t2_age, t1_rating,
                                            t2_rating, t1_event_rating, t2_event_rating,
                                            
                                            t1_rounds_lost_mirage, t1_rounds_won_mirage, t1_fp_mirage, t1_fp_percent_mirage,
                                            t1_winrate_mirage,t1_played_mirage,
                                            t1_5v4_mirage,t1_4v5_mirage,t1_pistol_mirage,
                                            t1_rounds_lost_inferno, t1_rounds_won_inferno, t1_fp_inferno, t1_fp_percent_inferno,
                                            t1_winrate_inferno,t1_played_inferno,
                                            t1_5v4_inferno,t1_4v5_inferno,t1_pistol_inferno,
                                            t1_rounds_lost_nuke, t1_rounds_won_nuke, t1_fp_nuke, t1_fp_percent_nuke,
                                            t1_winrate_nuke,t1_played_nuke,
                                            t1_5v4_nuke,t1_4v5_nuke,t1_pistol_nuke,
                                            t1_rounds_lost_overpass, t1_rounds_won_overpass, t1_fp_overpass, t1_fp_percent_overpass,
                                            t1_winrate_overpass,t1_played_overpass,
                                            t1_5v4_overpass,t1_4v5_overpass,t1_pistol_overpass,
                                            t1_rounds_lost_vertigo, t1_rounds_won_vertigo, t1_fp_vertigo, t1_fp_percent_vertigo,
                                            t1_winrate_vertigo,t1_played_vertigo,
                                            t1_5v4_vertigo,t1_4v5_vertigo,t1_pistol_vertigo,
                                            t1_rounds_lost_ancient, t1_rounds_won_ancient, t1_fp_ancient, t1_fp_percent_ancient,
                                            t1_winrate_ancient,t1_played_ancient,
                                            t1_5v4_ancient,t1_4v5_ancient,t1_pistol_ancient,
                                            t1_rounds_lost_anubis, t1_rounds_won_anubis, t1_fp_anubis, t1_fp_percent_anubis,
                                            t1_winrate_anubis,t1_played_anubis,
                                            t1_5v4_anubis,t1_4v5_anubis,t1_pistol_anubis,
                    
                                            t2_rounds_lost_mirage, t2_rounds_won_mirage, t2_fp_mirage, t2_fp_percent_mirage,
                                            t2_winrate_mirage,t2_played_mirage,
                                            t2_5v4_mirage,t2_4v5_mirage,t2_pistol_mirage,
                                            t2_rounds_lost_inferno, t2_rounds_won_inferno, t2_fp_inferno, t2_fp_percent_inferno,
                                            t2_winrate_inferno,t2_played_inferno,
                                            t2_5v4_inferno,t2_4v5_inferno,t2_pistol_inferno,
                                            t2_rounds_lost_nuke, t2_rounds_won_nuke, t2_fp_nuke, t2_fp_percent_nuke,
                                            t2_winrate_nuke,t2_played_nuke,
                                            t2_5v4_nuke,t2_4v5_nuke,t2_pistol_nuke,
                                            t2_rounds_lost_overpass, t2_rounds_won_overpass, t2_fp_overpass, t2_fp_percent_overpass,
                                            t2_winrate_overpass,t2_played_overpass,
                                            t2_5v4_overpass,t2_4v5_overpass,t2_pistol_overpass,
                                            t2_rounds_lost_vertigo, t2_rounds_won_vertigo, t2_fp_vertigo, t2_fp_percent_vertigo,
                                            t2_winrate_vertigo,t2_played_vertigo,
                                            t2_5v4_vertigo,t2_4v5_vertigo,t2_pistol_vertigo,
                                            t2_rounds_lost_ancient, t2_rounds_won_ancient, t2_fp_ancient, t2_fp_percent_ancient,
                                            t2_winrate_ancient,t2_played_ancient,
                                            t2_5v4_ancient,t2_4v5_ancient,t2_pistol_ancient,
                                            t2_rounds_lost_anubis, t2_rounds_won_anubis, t2_fp_anubis, t2_fp_percent_anubis,
                                            t2_winrate_anubis,t2_played_anubis,
                                            t2_5v4_anubis,t2_4v5_anubis,t2_pistol_anubis
                                            )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """)
        
        
    data_to_insert = (match,team_names[0], team_names[1], team_rating[0], team_rating[1],
                      ranking[0], ranking[1], matches_winstreak[0], matches_winstreak[1],
                      h2h[0], h2h[1], weeks[0], weeks[1], age[0], age[1],
                      rating_3m[0], rating_3m[1], rating_event[0], rating_event[1],

                      rounds_lost[0], rounds_won[0], first_pick[0], first_pick_pc[0],
                      winrate[0], maps_played[0], _5v4[0], _4v5[0], pistol[0],
                      rounds_lost[1], rounds_won[1], first_pick[2], first_pick_pc[2],
                      winrate[2], maps_played[2], _5v4[1], _4v5[1], pistol[1],
                      rounds_lost[2], rounds_won[2], first_pick[4], first_pick_pc[4],
                      winrate[4], maps_played[4], _5v4[2], _4v5[2], pistol[2],
                      rounds_lost[3], rounds_won[3], first_pick[6], first_pick_pc[6],
                      winrate[6], maps_played[6], _5v4[3], _4v5[3], pistol[3],
                      rounds_lost[4], rounds_won[4], first_pick[8], first_pick_pc[8],
                      winrate[8], maps_played[8], _5v4[4], _4v5[4], pistol[4],
                      rounds_lost[5], rounds_won[5], first_pick[10], first_pick_pc[10],
                      winrate[10], maps_played[10], _5v4[5], _4v5[5], pistol[5],
                      rounds_lost[6], rounds_won[6], first_pick[12], first_pick_pc[12],
                      winrate[12], maps_played[12], _5v4[6], _4v5[6], pistol[6],

                      rounds_lost[7], rounds_won[7], first_pick[1], first_pick_pc[1],
                      winrate[1], maps_played[1], _5v4[7], _4v5[7], pistol[7],
                      rounds_lost[8], rounds_won[8], first_pick[3], first_pick_pc[3],
                      winrate[3], maps_played[3], _5v4[8], _4v5[8], pistol[8],
                      rounds_lost[9], rounds_won[9], first_pick[5], first_pick_pc[5],
                      winrate[5], maps_played[5], _5v4[9], _4v5[9], pistol[9],
                      rounds_lost[10], rounds_won[10], first_pick[7], first_pick_pc[7],
                      winrate[7], maps_played[7], _5v4[10], _4v5[10], pistol[10],
                      rounds_lost[11], rounds_won[11], first_pick[9], first_pick_pc[9],
                      winrate[9], maps_played[9], _5v4[11], _4v5[11], pistol[11],
                      rounds_lost[12], rounds_won[12], first_pick[11], first_pick_pc[11],
                      winrate[11], maps_played[11], _5v4[12], _4v5[12], pistol[12],
                      rounds_lost[13], rounds_won[13], first_pick[13], first_pick_pc[13],
                      winrate[13], maps_played[13], _5v4[13], _4v5[13], pistol[13])

    cur.execute(insert_query, data_to_insert)
    conn.commit()
    
cur.close()
conn.close()
