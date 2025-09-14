import whisper
import json

model = whisper.load_model("large-v2")

result = model.transcribe(
    audio=r"C:\Users\bhavy\Videos RAG\downloads\Sample\How a Coder Plays Google Chrome’s T-rex Game Using JavaScript! #shorts.mp3",
    language="hi",
    task="translate",
    word_timestamps = False
)

print(result["segments"])
chunks = []
for segment in result["segments"]:
    chunks.append({"start": segment["start"], "end": segment["end"], "text": segment["text"]})

print(chunks)

with open("output.json", "w") as f:
    json.dump(chunks, f)


