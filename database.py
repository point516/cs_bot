import psycopg2

conn = psycopg2.connect(host="localhost", dbname='postgres', user='postgres', password='123456', port=5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS dataset (
    id SERIAL PRIMARY KEY,
    t1_h2h REAL,
    t2_h2h REAL, 
    t1_winstreak REAL,
    t2_winstreak REAL,
    t1_ranking REAL,
    t2_ranking REAL,
    t1_weeks REAL,
    t2_weeks REAL,
    t1_winrate REAL,
    t2_winrate REAL,
    t1_age REAL,
    t2_age REAL,
    t1_map_winrate REAL,
    t2_map_winrate REAL,
    t1_5v4 REAL,
    t2_5v4 REAL,
    t1_4v5 REAL,
    t2_4v5 REAL,
    t1_pistol REAL,
    t2_pistol REAL,
    t1_maps REAL,
    t2_maps REAL,
    t1_rating REAL,
    t2_rating REAL,
    t1_coef REAL DEFAULT 0.0,
    t2_coef REAL DEFAULT 0.0,
    
    win BOOLEAN
);
""")

conn.commit()

cur.close()
conn.close()