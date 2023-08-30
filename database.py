import psycopg2
from parsing import Parser

class Database:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to the database")
        except psycopg2.Error as e:
            print("Error: Unable to connect to the database")
            print(e)

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            print('Success')
        except psycopg2.Error as e:
            print("Error executing query:")
            print(e)

    def fill_dataset(self, event_name):
        parser = Parser()
        parser.start_driver()

        team_names, y_true, maps, num_maps, winstreak, h2h, ranking, weeks, age, \
                map_winrate, maps_played, _5v4, _4v5, pistol, rating_3m = parser.parse_event("https://hltv.org", event_name)

        stat_index = 0
        map_index = 0
        for match_index in range(len(num_maps)):
            team_info = (team_names[match_index*2], team_names[match_index*2+1], winstreak[match_index*2], winstreak[match_index*2+1], 
                        h2h[match_index*2], h2h[match_index*2+1], ranking[match_index*2], ranking[match_index*2+1], 
                        weeks[match_index*2], weeks[match_index*2+1], age[match_index*2], age[match_index*2+1], 
                        rating_3m[match_index*2], rating_3m[match_index*2+1])
            for index in range(num_maps[match_index]):
                insert_query = ("""INSERT INTO dataset (t1_name,t2_name,t1_winstreak,t2_winstreak,t1_h2h,t2_h2h,
                            t1_ranking,t2_ranking,t1_weeks,t2_weeks,t1_age,t2_age,t1_rating,t2_rating,map_name,
                            t1_winrate,t2_winrate,t1_maps,t2_maps,t1_5v4,t2_5v4,t1_4v5,t2_4v5,t1_pistol,t2_pistol,win)
                                
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                    """)
                map_info = (maps[map_index], map_winrate[stat_index], map_winrate[stat_index+num_maps[match_index]], maps_played[stat_index], maps_played[stat_index+num_maps[match_index]],
                            _5v4[stat_index], _5v4[stat_index+num_maps[match_index]], _4v5[stat_index], _4v5[stat_index+num_maps[match_index]], pistol[stat_index], pistol[stat_index+num_maps[match_index]],
                            not(bool(y_true[map_index])))    
                
                data_to_insert = team_info + map_info

                self.execute_query(insert_query, data_to_insert)

                stat_index += 1
                map_index += 1
            stat_index += num_maps[match_index]
        self.disconnect()
    
    def fill_event(self, event_name, table_name):
        parser = Parser()
        parser.start_driver()

        teams, team_rating, event_rating = parser.parse_event_rating("https://hltv.org", event_name)
        for index in range(len(teams)):
            insert_query = (f"""INSERT INTO {table_name} (team, team_rating, event_rating)
                            VALUES (%s,%s,%s);
                        """)
                
                
            data_to_insert = (teams[index], team_rating[index], event_rating[index])

            self.execute_query(insert_query, data_to_insert)

    def fill_bet(self, url):
        parser = Parser()
        parser.start_driver()

        team_names, rounds_lost, rounds_won, first_pick, first_pick_pc = parser.parse_bet(url)
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

            self.execute_query(insert_query, data_to_insert)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database")

if __name__ == "__main__":

    db = Database(dbname='postgres',
              user='postgres',
              password='123456',
              host="localhost",
              port=5432)
    db.connect()

    db.fill_bet('https://www.hltv.org/betting/analytics/2366099/apeks-vs-m80-esl-pro-league-season-18')
