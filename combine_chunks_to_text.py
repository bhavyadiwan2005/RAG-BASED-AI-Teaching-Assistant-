import json
import os

def add_combined_text_to_json(json_folder_path):
    """
    Add combined text field to each JSON file by combining all chunks
    """
    # Get all JSON files in the jsons folder
    json_files = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]
    
    print(f"Found {len(json_files)} JSON files to process")
    
    for json_file in json_files:
        json_path = os.path.join(json_folder_path, json_file)
        
        # Read the JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract title and chunks
        title = data.get('title', 'Unknown')
        chunks = data.get('chunks', [])
        
        # Combine all chunk texts
        combined_text = ""
        for chunk in chunks:
            text = chunk.get('text', '').strip()
            if text:
                combined_text += text + " "
        
        # Clean up the combined text
        combined_text = combined_text.strip()
        
        # Add combined_text field to the data
        data['combined_text'] = combined_text
        data['total_chunks'] = len(chunks)
        data['text_length'] = len(combined_text)
        
        # Save the updated JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated JSON file: {json_file}")
        print(f"   - Title: {title}")
        print(f"   - Chunks: {len(chunks)}")
        print(f"   - Text length: {len(combined_text)} characters\n")
    
    print(f"🎉 Successfully updated {len(json_files)} JSON files!")
    print(f"📁 All files updated in: {json_folder_path}")

if __name__ == "__main__":
    # Path to your jsons folder
    jsons_folder = r"C:\Users\bhavy\Videos RAG\jsons"
    
    if os.path.exists(jsons_folder):
        add_combined_text_to_json(jsons_folder)
    else:
        print(f"❌ Folder not found: {jsons_folder}")
        print("Please check the path and try again.")
