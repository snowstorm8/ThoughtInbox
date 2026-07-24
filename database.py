import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('thoughts.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS thoughts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
                            """)
        
        self.conn.commit()
        
    
    def add_thought(self, text):
        self.cursor.execute("INSERT INTO thoughts(text) VALUES(?)", (text,))
        self.conn.commit()
        
    def get_thoughts(self):
        self.cursor.execute("SELECT id, text, created FROM thoughts ORDER BY created DESC")
        
        return self.cursor.fetchall()
    
    def delete(self, thought_id):
        self.cursor.execute("DELETE FROM thoughts WHERE id = ?", (thought_id,))
        self.conn.commit()
        
    def update(self, thought_id, text):
        self.cursor.execute("UPDATE thoughts SET text = ? WHERE id = ?", (text, thought_id))
        self.conn.commit()