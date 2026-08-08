import json 
import psycopg

with open("spell_list.json", "r") as f:
    spells = json.load(f)
    print("ok")

conn = psycopg.connect(
    host="postgres",
    port=5432,
    dbname="dnd",
    user="postgres",
    password="password"
)

with conn.cursor() as cur:
    for spell in spells:
        cur.execute(
            
            """
            INSERT INTO spells (name, source, type, casting_time, range, components, duration, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                spell['name'],
                spell['source'],
                spell['type'],
                spell['casting_time'],
                spell['range'],
                spell['components'],
                spell['duration'],
                spell['description']
            )
        )

conn.commit()
conn.close()