# Crée, pour chaque participant, le petit fichier d'installation (manifeste) de la fausse appli,
# ainsi que la liste des liens à transmettre aux participants.
# A lancer UNE FOIS, dans le dossier de la fausse appli, après avoir copié dedans le fichier
# mapping_key_to_subId.js de la VRAIE appli (pour que les numéros soient les mêmes).

import csv
import json
import os

# ---------- A REMPLACER ----------
APP_NAME = "Space Gold"  # EXACTEMENT le même nom que la vraie appli
BASE_URL = "https://de-zhou.github.io/FakeApp"  # adresse du site de la fausse appli, sans "/" à la fin
# ---------------------------------

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("mapping_key_to_subId.js", "r", encoding="utf-8") as f:
    text = f.read()
mapping = json.loads(text[text.index("{"):])  # {code du lien: numéro de participant}

os.makedirs("manifests", exist_ok=True)
for file in os.listdir("manifests"):
    os.remove(os.path.join("manifests", file))

rows = []
for key, sub_id in mapping.items():
    start_url = BASE_URL + "/index.html?subId=" + key
    manifest = {
        "id": start_url,
        "name": APP_NAME,
        "short_name": APP_NAME,
        "start_url": start_url,
        "scope": BASE_URL + "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#ffffff",
        "icons": [
            {"src": BASE_URL + "/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": BASE_URL + "/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    with open("manifests/manifest_" + key + ".json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    rows.append([sub_id, start_url, key])

rows.sort(key=lambda r: int(r[0]))
with open("liens_fausse_appli.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Sub_ID", "URL", "key_code"])
    w.writerows(rows)

print(len(rows), "manifestes créés dans le dossier manifests/")
print("Liste des liens : liens_fausse_appli.csv")
