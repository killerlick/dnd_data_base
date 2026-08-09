from spell_database import scrape_spells
from insert_spells_database import insert_spells


def main():
    print("Starting scraper...")

    spells = scrape_spells()

    print(f"{len(spells)} spells scraped.")

    print("Inserting spells into PostgreSQL...")

    insert_spells(spells)

    print("Done.")


if __name__ == "__main__":
    main()