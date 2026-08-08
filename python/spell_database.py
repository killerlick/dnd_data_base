import requests as req
import bs4 as bs
import json
from itertools import islice

index = 0
base_url : str= "https://dnd5e.wikidot.com"



r = req.get(base_url + "/spells")
soup = bs.BeautifulSoup(r.text, "html.parser")
spell_list = soup.find_all("a", href=lambda x: x and "spell:" in x)
spell_list_json = []

def write_spell_page(href):
    with open("output.html", "w") as f:
        r_spell = req.get(base_url + href)
        f.write(r_spell.text)

for spell in spell_list:
    try:
        r_spell = req.get(base_url + spell['href'])
        soup_spell = bs.BeautifulSoup(r_spell.text, "html.parser")

        spell_name = soup_spell.find_all("div", class_="page-title")[0].text
        spell_source = soup_spell.find_all("p", string = lambda text:text and text.startswith("Source:"))[0].text.replace("Source: ", "")
        spell_type = soup_spell.select_one("p em").text

        t = soup_spell.select_one("p strong").parent.text.split("\n")
        #print(t)
        if len(t) < 4:
            t= soup_spell.select("p strong")
            spell_casting_time = t[0].parent.text.replace("Casting Time: ", "")
            spell_range = t[1].parent.text.replace("Range: ", "")
            spell_components = t[2].parent.text.replace("Components: ", "")
            spell_duration = t[3].parent.text.replace("Duration: ", "")
        else:
            spell_casting_time = t[0].replace("Casting Time: ", "")
            spell_range = t[1].replace("Range: ", "")
            spell_components = t[2].replace("Components: ", "")
            spell_duration = t[3].replace("Duration: ", "")
        #print(soup_spell.find("div", id="page-content").text.split("<p>")[0].split("\n")[8]  )
        #todo ajouter un truc pour récupérer la description du sort, car actuellement ça ne fonctionne pas(array precise de la description du sort)
        spell_description = soup_spell.find("div", id="page-content").text.split("<p>")[0].split("\n")[8]

        spell_url = r_spell.url
        spell_list_json.append(
        {
            'name': spell_name,
            'url': spell_url,
            'source': spell_source,
            'type': spell_type,
            'casting_time': spell_casting_time,
            'range': spell_range,
            'components': spell_components,
            'duration': spell_duration,
            'description': spell_description
        }
        )
    except Exception as e:
        print(f"Error processing spell {spell['href']}: {e}")
        #write_spell_page(spell['href'])
        print(spell['href'])
        print(index)
        break

    #if index == 150:
    #    break
    index += 1

with open("spell_list.json", "w") as f:
    json.dump(spell_list_json, f,indent=3)

