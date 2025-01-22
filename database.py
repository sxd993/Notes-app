import sqlite3

conn = sqlite3.connect('/Users/vladimir/Python/NotesApp/notes.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
            )'''
)

conn.commit()
cur.close()
conn.close()