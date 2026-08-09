import requests as req
import bs4 as bs
import json


BASE_URL: str = "https://dnd5e.wikidot.com"

#permet d'avoir TOUT le html du site
def get_soup(url):
    response = req.get(url)
    response.raise_for_status()
    return bs.BeautifulSoup(response.text, "html.parser")

#return tableau des balise a href des sorts
def get_spell_list_hrefs():
    soup = get_soup(BASE_URL + "/spells")

    return soup.find_all(
        "a",
        href=lambda x: x and "spell:" in x
    )


#return un dictionnaire avec les infos du sort
def get_spell_data(href):
    soup = get_soup(BASE_URL + href)

    spell_name = soup.find(
        "div",
        class_="page-title"
    ).text.strip()

    spell_source = soup.find(
        "p",
        string=lambda text: text and text.startswith("Source:")
    ).text.replace("Source: ", "").strip()

    spell_type = soup.select_one("p em").text.strip()

    t = soup.select_one("p strong").parent.text.split("\n")

    if len(t) < 4:
        t = soup.select("p strong")

        spell_casting_time = t[0].parent.text.replace(
            "Casting Time: ", ""
        ).strip()

        spell_range = t[1].parent.text.replace(
            "Range: ", ""
        ).strip()

        spell_components = t[2].parent.text.replace(
            "Components: ", ""
        ).strip()

        spell_duration = t[3].parent.text.replace(
            "Duration: ", ""
        ).strip()

    else:
        spell_casting_time = t[0].replace(
            "Casting Time: ", ""
        ).strip()

        spell_range = t[1].replace(
            "Range: ", ""
        ).strip()

        spell_components = t[2].replace(
            "Components: ", ""
        ).strip()

        spell_duration = t[3].replace(
            "Duration: ", ""
        ).strip()

    spell_description = (
        soup
        .find("div", id="page-content")
        .text
        .split("<p>")[0]
        .split("\n")[8]
    )

    return {
        "name": spell_name,
        "url": BASE_URL + href,
        "source": spell_source,
        "type": spell_type,
        "casting_time": spell_casting_time,
        "range": spell_range,
        "components": spell_components,
        "duration": spell_duration,
        "description": spell_description
    }


#return un tableau de dictionnaire avec les infos de tous les sorts
def scrape_spells():
    spell_list_json = []

    spell_list = get_spell_list_hrefs()

    for index, spell in enumerate(spell_list):
        try:
            spell_data = get_spell_data(spell["href"])
            spell_list_json.append(spell_data)

        except Exception as e:
            print(
                f"Error processing spell {spell['href']}: {e}"
            )
            print(f"Index: {index}")

            break

    return spell_list_json

#sauvegarde le tableau de dictionnaire (spells) dans un fichier json
def save_spells(spells, filename="spell_list.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            spells,
            f,
            indent=3,
            ensure_ascii=False
        )


def main():
    spells = scrape_spells()
    save_spells(spells)

    print(f"{len(spells)} spells saved.")


if __name__ == "__main__":
    main()
