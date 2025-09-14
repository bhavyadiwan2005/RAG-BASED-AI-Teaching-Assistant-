import requests
import os
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib

def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    embedding = r.json()["embeddings"] 
    return embedding

# Load mapping from json filename to title and number
with open("output.json", encoding="utf-8") as f:
    output_data = json.load(f)
file_info = {}
for audio in output_data["audio_files"]:
    file_info[audio["json_file"]] = {
        "title": audio["title"],
        "number": audio["audio_number"]
    }

jsons = [f for f in os.listdir("jsons") if f.endswith('.json')]
my_dicts = []
chunk_id = 0

for json_file in jsons:
    try:
        with open(f"jsons/{json_file}", encoding="utf-8") as f:
            content_str = f.read().strip()
            if not content_str:
                print(f"Skipping empty file: {json_file}")
                continue
            content = json.loads(content_str)
        print(f"Creating Embeddings for {json_file}")
        embeddings = create_embedding([c['text'] for c in content['chunks']])
        for i, chunk in enumerate(content['chunks']):
            chunk['chunk_id'] = chunk_id
            chunk['embedding'] = embeddings[i]
            # Add title and number from mapping
            chunk['title'] = file_info.get(json_file, {}).get('title', '')
            chunk['number'] = file_info.get(json_file, {}).get('number', '')
            chunk_id += 1
            my_dicts.append(chunk)
    except Exception as e:
        print(f"Error processing {json_file}: {e}")

df = pd.DataFrame.from_records(my_dicts)

# save this in data frame
joblib.dump(df, "embeddings.joblib")
# print(df)
