import sqlite3
import sys

def query_brain(search_term):
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    
    # Simple semantic keyword matching across stored content and AI summaries
    cursor.execute('''
        SELECT new_path, category, summary FROM file_ledger 
        WHERE content LIKE ? OR summary LIKE ?
    ''', (f'%{search_term}%', f'%{search_term}%'))
    
    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"No memories found for: '{search_term}'")
        return

    print(f"\n--- Found {len(results)} matches in your Second Brain ---")
    for path, cat, summary in results:
        print(f"Location: {path} [{cat.upper()}]")
        print(f"AI Context: {summary}\n")

if __name__ == "__main__":
    term = sys.argv[1] if len(sys.argv) > 1 else input("What do you want to remember? ")
    query_brain(term)