from parsing import Parser
import psycopg2

conn = psycopg2.connect(host="localhost", dbname='postgres', user='postgres', password='123456', port=5432)
cur = conn.cursor()

parser = Parser()
parser.start_driver()

team_names, y_true, maps, num_maps, winstreak, h2h, ranking, weeks, age, \
        map_winrate, maps_played, _5v4, _4v5, pistol, rating_3m = parser.parse_event("https://hltv.org","blast fall groups 2023")

for match_index in range(len(num_maps)):
    team_info = (team_names[match_index*2], team_names[match_index*2+1], winstreak[match_index*2], winstreak[match_index*2+1], 
                 h2h[match_index*2], h2h[match_index*2+1], ranking[match_index*2], ranking[match_index*2+1], 
                 weeks[match_index*2], weeks[match_index*2+1], age[match_index*2], age[match_index*2+1], 
                 rating_3m[match_index*2], rating_3m[match_index*2+1],)
    for index in range(num_maps[match_index]):
        insert_query = ("""INSERT INTO dataset (t1_name,t2_name,t1_winstreak,t2_winstreak,t1_h2h,t2_h2h,
                    t1_ranking,t2_ranking,t1_weeks,t2_weeks,t1_age,t2_age,t1_rating,t2_rating,map_name,
                    t1_winrate,t2_winrate,t1_5v4,t2_5v4,t1_4v5,t2_4v5,t1_pistol,t2_pistol,t1_maps,t2_maps)
                        
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """)
        
        map_info = ()
