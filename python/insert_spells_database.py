import json
import psycopg


#return un tableau de dictionnaire avec les infos de tous les sorts
def load_spells(filename="spell_list.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

#ajoute les sorts dans la base de données PostgreSQL
def insert_spells(spells):
    conn = psycopg.connect(
        host="postgres",
        port=5432,
        dbname="dnd",
        user="postgres",
        password="password"
    )

    try:
        with conn.cursor() as cur:
            for spell in spells:
                cur.execute(
                    """
                    INSERT INTO spells (
                        name,
                        source,
                        type,
                        casting_time,
                        range,
                        components,
                        duration,
                        description
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        spell["name"],
                        spell["source"],
                        spell["type"],
                        spell["casting_time"],
                        spell["range"],
                        spell["components"],
                        spell["duration"],
                        spell["description"]
                    )
                )

        conn.commit()

    finally:
        conn.close()


def main():
    spells = load_spells()
    insert_spells(spells)

    print("Spells inserted successfully")


if __name__ == "__main__":
    main()