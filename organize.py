import os
import shutil
import sqlite3
import urllib.request
import json
from datetime import datetime

# Our local LLM
OLLAMA_MODEL = "llama3.2:1b"

def init_db():
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_name TEXT,
            new_path TEXT,
            category TEXT,
            summary TEXT,
            content TEXT,
            processed_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def ask_ai_to_classify(filename, content):
    url = "http://localhost:11434/api/generate"
    
    # 1. PYTHON GRABS THE ORIGINAL EXTENSION NATIVELY
    # If filename is "info.txt", orig_ext becomes ".txt"
    _, orig_ext = os.path.splitext(filename)
    
    content_lower = content.lower()
    
    # 2. Deterministic Rule Matching for folder placement
    has_code_syntax = (
        "def " in content_lower or 
        "import " in content_lower or 
        "if __name__" in content_lower or
        "const " in content_lower
    )
    is_explicit_markdown = content_lower.startswith("#") or "###" in content_lower
    
    if has_code_syntax and not is_explicit_markdown:
        category = "code"
        fallback_topic = "python_script"
    else:
        category = "notes"
        fallback_topic = "project_notes"

    # 3. Ask the AI for a quick topic summary
    prompt = f"Provide a concise, 4-word summary or title describing the main subject of this text. Return ONLY the title, no other text:\n\n{content[:500]}"
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_res = json.loads(response.read().decode('utf-8'))
            ai_text = raw_res.get('response', '').strip().lower()
            
            clean_topic = "".join([c if c.isalnum() or c == " " else "" for c in ai_text])
            clean_topic = clean_topic.replace(" ", "_").strip("_")
            
            if not clean_topic or len(clean_topic) > 40:
                clean_topic = fallback_topic
                
            new_name = f"{clean_topic}_{int(datetime.now().timestamp())}{orig_ext}"
            summary = f"Ingested {category} file focused on {ai_text}."
            
            return category, new_name, summary
            
    except Exception as e:
        new_name = f"fallback_{fallback_topic}_{int(datetime.now().timestamp())}{orig_ext}"
        return category, new_name, "Ingested unstructured repository file via fallback route."

def tidy_inbox():
    init_db()
    inbox_dir = './inbox'
    base_target = './organized'
    
    if not os.path.exists(inbox_dir):
        os.makedirs(inbox_dir)
        print("Created empty inbox directory. Drop your files there.")
        return
        
    if not os.listdir(inbox_dir):
        print("Inbox folder is empty. Drop files in to test.")
        return

    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()

    for filename in os.listdir(inbox_dir):
        file_path = os.path.join(inbox_dir, filename)
        if os.path.isdir(file_path):
            continue

        print(f"Analyzing {filename} via local Ollama processing...")
        with open(file_path, 'r', errors='ignore') as f:
            content = f.read()

        category, new_name, summary = ask_ai_to_classify(filename, content)
        
        # Guard rails for target sorting directories
        if category not in ['code', 'notes']:
            category = 'notes'
            
        target_dir = os.path.join(base_target, category)
        os.makedirs(target_dir, exist_ok=True)
        new_path = os.path.join(target_dir, new_name)

        shutil.move(file_path, new_path)
        
        cursor.execute('''
            INSERT INTO file_ledger (original_name, new_path, category, summary, content, processed_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (filename, new_path, category, summary, content, datetime.now().isoformat()))
        
        print(f" [SUCCESS]: {filename} -> {new_path}")
        print(f"   Context: {summary}\n")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    tidy_inbox()