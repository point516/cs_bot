from parsing import Parser
import psycopg2

conn = psycopg2.connect(host="localhost", dbname='postgres', user='postgres', password='123456', port=5432)
cur = conn.cursor()

parser = Parser()
parser.start_driver()


# team_names, y_true, maps, num_maps, winstreak, h2h, ranking, weeks, age, \
#         map_winrate, maps_played, _5v4, _4v5, pistol, rating_3m = parser.parse_event("https://hltv.org","blast fall groups 2023")

# stat_index = 0
# map_index = 0
# for match_index in range(len(num_maps)):
#     team_info = (team_names[match_index*2], team_names[match_index*2+1], winstreak[match_index*2], winstreak[match_index*2+1], 
#                  h2h[match_index*2], h2h[match_index*2+1], ranking[match_index*2], ranking[match_index*2+1], 
#                  weeks[match_index*2], weeks[match_index*2+1], age[match_index*2], age[match_index*2+1], 
#                  rating_3m[match_index*2], rating_3m[match_index*2+1])
#     for index in range(num_maps[match_index]):
#         insert_query = ("""INSERT INTO dataset (t1_name,t2_name,t1_winstreak,t2_winstreak,t1_h2h,t2_h2h,
#                     t1_ranking,t2_ranking,t1_weeks,t2_weeks,t1_age,t2_age,t1_rating,t2_rating,map_name,
#                     t1_winrate,t2_winrate,t1_maps,t2_maps,t1_5v4,t2_5v4,t1_4v5,t2_4v5,t1_pistol,t2_pistol,win)
                        
#                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
#             """)
        
#         map_info = (maps[map_index], map_winrate[stat_index], map_winrate[stat_index+2], maps_played[stat_index], maps_played[stat_index+2],
#                     _5v4[stat_index], _5v4[stat_index+2], _4v5[stat_index], _4v5[stat_index+2], pistol[stat_index], pistol[stat_index+2],
#                     not(bool(y_true[map_index])))    
        
#         data_to_insert = team_info + map_info

#         cur.execute(insert_query, data_to_insert)
#         conn.commit()

#         stat_index += 1
#         map_index += 1
#     stat_index += 2


# teams, team_rating, event_rating = parser.parse_event_rating("https://hltv.org", "blast fall groups 2023")
# for index in range(len(teams)):
#     insert_query = ("""INSERT INTO blast_fall_groups2023_rating (team, team_rating, event_rating)
#                      VALUES (%s,%s,%s);
#                 """)
        
        
#     data_to_insert = (teams[index], team_rating[index], event_rating[index])

#     cur.execute(insert_query, data_to_insert)
#     conn.commit()


team_names, rounds_lost, rounds_won, first_pick, first_pick_pc = parser.parse_bet('https://www.hltv.org/betting/analytics/2365868/furia-academy-vs-meta-cct-south-america-series-9')
for index in range(len(team_names)):
    insert_query = ("""INSERT INTO betting_info (
                                            team, rounds_lost_mirage, rounds_won_mirage, fp_mirage, fp_percent_mirage,
                                            rounds_lost_inferno, rounds_won_inferno, fp_inferno, fp_percent_inferno,
                                            rounds_lost_nuke, rounds_won_nuke, fp_nuke, fp_percent_nuke,
                                            rounds_lost_overpass, rounds_won_overpass, fp_overpass, fp_percent_overpass,
                                            rounds_lost_vertigo, rounds_won_vertigo, fp_vertigo, fp_percent_vertigo,
                                            rounds_lost_ancient, rounds_won_ancient, fp_ancient, fp_percent_ancient,
                                            rounds_lost_anubis, rounds_won_anubis, fp_anubis, fp_percent_anubis
                                                )
                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                 """)
        
        
    data_to_insert = (team_names[index], rounds_lost[index*7], rounds_won[index*7], first_pick[index], first_pick_pc[index],
                      rounds_lost[index*7+1], rounds_won[index*7+1], first_pick[index+2], first_pick_pc[index+2],
                      rounds_lost[index*7+2], rounds_won[index*7+2], first_pick[index+4], first_pick_pc[index+4],
                      rounds_lost[index*7+3], rounds_won[index*7+3], first_pick[index+6], first_pick_pc[index+6],
                      rounds_lost[index*7+4], rounds_won[index*7+4], first_pick[index+8], first_pick_pc[index+8],
                      rounds_lost[index*7+5], rounds_won[index*7+5], first_pick[index+10], first_pick_pc[index+10],
                      rounds_lost[index*7+6], rounds_won[index*7+6], first_pick[index+12], first_pick_pc[index+12],)

    cur.execute(insert_query, data_to_insert)
    conn.commit()