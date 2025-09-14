import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import requests


def create_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    embedding = r.json()["embeddings"] 
    return embedding

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "deepseek-r1", 
        "prompt": prompt,
        "stream": False,
    })
    try:
        response_json = r.json()
        print("Full API response:", response_json)
        response_text = response_json.get("response", None)  # <-- FIXED
        if response_text is None:
            print("❌ 'response' key not found in response.")
            return ""
        return response_text
    except Exception as e:
        print("❌ Error parsing response:", e)
        return ""

df =joblib.load("embeddings.joblib")


incoming_query = input("Ask a Question: ")
question_embedding = create_embedding([incoming_query])[0] 

similarities = cosine_similarity(np.vstack(df['embedding']), [question_embedding]).flatten()
print(similarities)
top_results = 5
max_indx = similarities.argsort()[::-1][0:top_results]
print(max_indx)
new_df = df.loc[max_indx] 
print(new_df[["title", "number", "text"]])

prompt = f''' here are  video chunks containing video title , video number ,  start time and end time in seconds , the text at that time:

{new_df[['title' , 'number' , 'start' , 'end' , 'text']].to_json(orient = 'records')}
-----------------------------

"{incoming_query}"
user asked this question related to the video chunks , you have to answer where and how much content is taught where in which video and at what time stamp , and guide the user to go to that particular video and 
time stamp to get the answer . If user asks unrelated question to the video chunks , you have to say that the answer is not in the video chunks and you dont know the answer to that question .

'''
with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)
    
response  = inference(prompt)
print("Response: ", response)

with open("response.txt", "w", encoding="utf-8") as f:
    f.write(response)
# for index , item in new_df.iterrows():
#     print(index , item['title'] , item['number'] , item['text'] , item['start'] , item['end'])