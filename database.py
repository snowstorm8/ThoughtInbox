import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('thoughts.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS thoughts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            favorite INTEGER DEFAULT 0
        )
                            """)
        
        self.conn.commit()
        
        try:
            self.cursor.execute("ALTER TABLE thoughts ADD COLUMN favorite INTEGER DEFAULT 0")
            self.conn.commit()
        except Exception:
            pass
    
    def add_thought(self, text):
        self.cursor.execute("INSERT INTO thoughts(text) VALUES(?)", (text,))
        self.conn.commit()
        
    def restore_thought(self, text, created, favorite):
        self.cursor.execute("INSERT INTO thoughts(text, created, favorite) VALUES(?, ?)", (text, created, favorite))
        self.conn.commit()    
        
    def get_thoughts(self):
        self.cursor.execute("SELECT id, text, created, favorite FROM thoughts ORDER BY created DESC")
        
        return self.cursor.fetchall()
    
    def get_thought(self, thought_id):
        self.cursor.execute("SELECT id, text, created, favorite FROM thoughts WHERE id = ?", (thought_id,))
        return self.cursor.fetchone()
    
    def delete(self, thought_id):
        self.cursor.execute("DELETE FROM thoughts WHERE id = ?", (thought_id,))
        self.conn.commit()
        
    def update(self, thought_id, text):
        self.cursor.execute("UPDATE thoughts SET text = ? WHERE id = ?", (text, thought_id))
        self.conn.commit()
        
    def search(self, query):
        self.cursor.execute("SELECT id, text, created, favorite FROM thoughts WHERE text LIKE ? ORDER BY created DESC", (f"%{query}%",))
        return self.cursor.fetchall()
    
    def toggle_favorite(self, thought_id):
        self.cursor.execute("UPDATE thoughts SET favorite = CASE WHEN favorite = 1 THEN 0 ELSE 1 END WHERE id = ?", (thought_id,))
        self.conn.commit()
        
    def get_only_favorite(self):
        self.cursor.execute("SELECT id, text, created, favorite FROM thoughts WHERE favorite = 1 ORDER BY created DESC")
        self.conn.commit()
        
    def is_favorite(self, thought_id):
        self.cursor.execute("SELECT favorite FROM thoughts WHERE id = ?", (thought_id,))
        result = self.cursor.fetchone()
        return bool(result[0]) if result else False
    
    def close(self):
        self.conn.close()