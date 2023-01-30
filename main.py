import requests
import json
import re

# Ricordarsi di impostare il path cartella cpk anche in ./resources/properties/pywaldo_service_config.ini come segue
# [SenseiConfig]
# cpk_path=./resources/cpk/experiment_3903_model_(it)/standard_it_16.0.3/tv-1_it_1642453027



# Caricamento cartella cpk estratta da archivio CPK contenuto in archivio MLPK
cpk_folder = "C:/Users/smarotta/OneDrive - Expert.ai S.p.A/MIRCO/pywaldoservice/pywaldo/resources/cpk/experiment_3903_model_(it)/standard_it_16.0.3/tv-1_it_1642453027"

cpk_payload = {"path": cpk_folder}

cpk_post = requests.post("http://127.0.0.1:8000/apis/cogito", json=cpk_payload)
print(cpk_post)



# Caricamento modello .mod estratto da archivio MLPK
model_file = "C:/Users/smarotta/Downloads/96b25ea4-7abb-4f8a-a5e5-fb3cf790b0a3.mod"

model_payload = {
    "path": "C:/Users/smarotta/Downloads/96b25ea4-7abb-4f8a-a5e5-fb3cf790b0a3.mod",
    "model_id": "96b25ea4-7abb-4f8a-a5e5-fb3cf790b0a3"  # può essere qualsiasi cosa
}

model_post = requests.post("http://127.0.0.1:8000/apis/model", json=model_payload)
print(model_post)



# Uso modello
testo_completo = """S0: Russian forces have established a presence in the eastern part of the town.
  S1: Our units continue their advance toward Vuhledar."""

# Divido trascrizione in sentences
sentences_testo = [s.strip() for s in re.split(r"S\d+:", testo_completo)][1:]

print(sentences_testo)

# per ogni sentence estraggo le categorie
output = []
for s in sentences_testo:
    pred_payload = {
        "text_document": s,
        "configuration": {
            "load_from_model": True,
            "full_prediction_output": True
        }
    }

    pred = requests.post(f"http://127.0.0.1:8000/apis/analyze_and_apply/sync/{model_payload['model_id']}",
                     json=pred_payload)
    pred = pred.json()
    results = pred["results"].replace("\\", "")
    results_dict = json.loads(results)
    winner_categories = [k for k in results_dict[0]["annotations_list"]["winners"].keys()]
    print("WINNERS", winner_categories)
    explaination = [results_dict[0]["annotations_list"]["winners"][cat]["explain"] for cat in winner_categories]
    print("EXPLANATION", explaination)

    output.append({
      "sentence": s,
      "categories": winner_categories,
      "explaination": explaination
    })
print(output)
