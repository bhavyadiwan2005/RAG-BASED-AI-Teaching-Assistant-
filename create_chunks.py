import whisper
import json
import os

model = whisper.load_model("large-v2")

# Create JSON folder if it doesn't exist
json_folder = r"C:\Users\bhavy\Videos RAG\jsons"
if not os.path.exists(json_folder):
    os.makedirs(json_folder)
    print(f"Created folder: {json_folder}")

# Get list of audio files (excluding subfolders like Sample)
audios = [f for f in os.listdir("downloads") if f.endswith('.mp3') and os.path.isfile(os.path.join("downloads", f))]
total_audios = len(audios)

print(f"Total number of audio files to process: {total_audios}")

# Initialize output data structure for summary
summary_data = {
    "total_audios": total_audios,
    "audio_files": []
}

for i, audio in enumerate(audios, 1):
    print(f"Processing audio {i}/{total_audios}: {audio}")
    
    # Extract audio title (remove .mp3 extension)
    audio_title = audio.replace('.mp3', '')
    
    result = model.transcribe(
        audio=f"downloads/{audio}",
        language="hi",
        task="translate",
        word_timestamps=False
    )

    chunks = []
    for segment in result["segments"]:
        chunks.append({"start": segment["start"], "end": segment["end"], "text": segment["text"]})

    # Create individual audio data
    audio_data = {
        "audio_number": i,
        "title": audio_title,
        "filename": audio,
        "chunks": chunks
    }
    
    # Save individual JSON file for this audio
    json_filename = f"{audio_title}.json"
    json_path = os.path.join(json_folder, json_filename)
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(audio_data, f, indent=2, ensure_ascii=False)
    
    # Add to summary data
    summary_data["audio_files"].append({
        "audio_number": i,
        "title": audio_title,
        "filename": audio,
        "json_file": json_filename
    })
    
    print(f"Completed processing: {audio_title}")
    print(f"Saved to: {json_path}")

# Save summary output
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(summary_data, f, indent=2, ensure_ascii=False)

print(f"\nProcessing complete! Processed {total_audios} audio files.")
print(f"Individual JSON files saved in '{json_folder}' folder")
print("Summary saved to output.json")
