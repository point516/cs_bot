from parsing import Parser
import psycopg2

conn = psycopg2.connect(host="localhost", dbname='postgres', user='postgres', password='123456', port=5432)
cur = conn.cursor()

len = 131
start = 16

maps = []
dataset = []

query = """
        SELECT dataset.map_name
        FROM dataset
        """
cur.execute(query)
for row in cur.fetchall():
    maps.append(row[0])

for index in range(len):
    query = f"""
            SELECT dataset.t1_winstreak,dataset.t2_winstreak,dataset.t1_h2h,dataset.t2_h2h,
                            dataset.t1_ranking,dataset.t2_ranking,dataset.t1_weeks,dataset.t2_weeks,dataset.t1_age,dataset.t2_age,dataset.t1_rating,dataset.t2_rating,
                            dataset.t1_winrate,dataset.t2_winrate,dataset.t1_5v4,dataset.t2_5v4,dataset.t1_4v5,dataset.t2_4v5,dataset.t1_maps,dataset.t2_maps,  
                            dataset.t1_pistol,dataset.t2_pistol,win,betting_info.rounds_lost_{maps[index]}, betting_info.rounds_won_{maps[index]}, betting_info.fp_{maps[index]}, betting_info.fp_percent_{maps[index]}
            FROM dataset
            FULL OUTER JOIN betting_info ON dataset.t1_name = betting_info.team
            WHERE dataset.id = {start+index}
            """
    cur.execute(query)
    row = cur.fetchall()[0]
    query = f"""
            SELECT betting_info.rounds_lost_{maps[index]}, betting_info.rounds_won_{maps[index]}, betting_info.fp_{maps[index]}, betting_info.fp_percent_{maps[index]}
            FROM dataset
            FULL OUTER JOIN betting_info ON dataset.t2_name = betting_info.team
            WHERE dataset.id = {start+index}
            """
    cur.execute(query)
    row += cur.fetchall()[0]

    if start+index < 73:

        query = f"""
                SELECT blast_fall_groups2023_rating.team_rating, blast_fall_groups2023_rating.event_rating
                FROM dataset
                FULL OUTER JOIN blast_fall_groups2023_rating ON dataset.t1_name = blast_fall_groups2023_rating.team
                WHERE dataset.id = {start+index}
                """
        cur.execute(query)
        row += cur.fetchall()[0]
        query = f"""
                SELECT blast_fall_groups2023_rating.team_rating, blast_fall_groups2023_rating.event_rating
                FROM dataset
                FULL OUTER JOIN blast_fall_groups2023_rating ON dataset.t2_name = blast_fall_groups2023_rating.team
                WHERE dataset.id = {start+index}
                """
        cur.execute(query)
        row += cur.fetchall()[0]

    elif start+index >= 73 and start+index < 147:

        query = f"""
                SELECT iem_cologne2023_rating.team_rating, iem_cologne2023_rating.event_rating
                FROM dataset
                FULL OUTER JOIN iem_cologne2023_rating ON dataset.t1_name = iem_cologne2023_rating.team
                WHERE dataset.id = {start+index}
                """
        cur.execute(query)
        row += cur.fetchall()[0]
        query = f"""
                SELECT iem_cologne2023_rating.team_rating, iem_cologne2023_rating.event_rating
                FROM dataset
                FULL OUTER JOIN iem_cologne2023_rating ON dataset.t2_name = iem_cologne2023_rating.team
                WHERE dataset.id = {start+index}
                """
        cur.execute(query)
        row += cur.fetchall()[0]

    dataset.append(row)
conn.close()

print(dataset[57])