# Local Folder Organizer and Search System

This is a simple system that automatically cleans up messy folders, puts files where they belong, and lets you search through them instantly. 

It uses a small AI model running directly on your computer through a program called Ollama. This means it is completely free, does not send your data to the internet, and works entirely offline.

## How it Works

The system is split into three main parts:

1. **The Organizer (organize.py):** This script looks inside your messy folder. It checks if a file is code or text notes by looking for programming keywords like "def" or "import". Once it decides what type of file it is, it asks the local AI to read the text and give it a short title. It then renames the file with that clean title, adds a time stamp, and moves it to the correct folder.
2. **The Background Worker (schedule_worker.py):** This script acts like a clock. When you run it, it keeps running in the background and triggers the organizer script every 5 minutes so you never have to clean your folders manually.
3. **The Search Engine (search.py):** Every time a file is moved, the system saves a copy of its text, its new location, and its AI summary into a local database file called brain.db. You can use this script to type a keyword and instantly see exactly where your file went without digging through folders.

## Folder Layout

```text
app/
│
├── inbox/                  # Put your messy, unorganized files here
│
├── organized/              # This is where your clean files go
│   ├── code/               # Contains your script files (like .py files)
│   └── notes/              # Contains your text notes (like .txt or .md files)
│
├── organize.py             # The main cleanup script
├── schedule_worker.py      # The timer script that keeps everything running
├── search.py               # The script you use to find your files later
└── brain.db                # The hidden database file that remembers everything
```

## Setup Instructions

### 1. Open the Folder in Terminal
Open your command prompt or terminal and change to your project folder:
```bash
cd path/to/your/folder
```

### 2. Set Up a Virtual Environment
Create and turn on a Python virtual environment to keep your project clean.

On Windows:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On Mac or Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install and Run Ollama
1. Download and install Ollama from its official website.
2. Open your terminal and run this command to download the tiny AI model:
```bash
ollama pull llama3.2:1b
```
Make sure the Ollama application is running on your computer before you start the scripts.

## How to Use the System

### Step 1: Add Messy Files
Drop any unorganized files into the **inbox** folder. You can use text files, python scripts, or markdown documents with random names.

### Step 2: Start the Automatic Cleanup
Run the background worker script in your terminal:
```powershell
python schedule_worker.py
```
The script will instantly check the inbox, process your files using the local AI, and organize them into the **organized** folder. It will keep running and check back every 5 minutes.

### Step 3: Stop the System
When you are done recording your video or testing the project, click inside your terminal window and press **Ctrl + C** on your keyboard to stop the automatic loop.

### Step 4: Search for Your Files
Because the system saves everything into a local database, you can search for words inside your files instantly. Open your terminal and type python search.py followed by the word you want to find.

For example:
```powershell
python search.py conversion
```

The terminal will print out the exact folder path of the file, what category it is, and a short summary of what is inside the file.