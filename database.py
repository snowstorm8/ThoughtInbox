import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('thoughts.db')
        
        self.conn.execute("PRAGMA foreign_keys = ON")
        
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS thoughts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            favorite INTEGER DEFAULT 0
        )
                            """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
                            """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS thought_tags(
            thought_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (thought_id, tag_id),
            FOREIGN KEY (thought_id) REFERENCES thoughts(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id)
        )
                            """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thought_id INTEGER NOT NULL,
            reminder_time TEXT NOT NULL,
            triggered INTEGER DEFAULT 0,
            FOREIGN KEY (thought_id) REFERENCES thoughts(id)
            ON DELETE CASCADE
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
        return self.cursor.lastrowid
        
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
        
    def search(self, query, favorites_only = False):
        sql = """
            SELECT id, text, created, favorite
            FROM thoughts
        """
        
        conditions = []
        parameters = []
        
        if query:
            conditions.append("text LIKE ?")
            parameters.append(f"%{query}%")
            
        if favorites_only:
            conditions.append("favorite = 1")
            
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
            
        sql += " ORDER BY created DESC"
        
        self.cursor.execute(sql, parameters)
        
        return self.cursor.fetchall()
    
    def toggle_favorite(self, thought_id):
        self.cursor.execute("UPDATE thoughts SET favorite = CASE WHEN favorite = 1 THEN 0 ELSE 1 END WHERE id = ?", (thought_id,))
        self.conn.commit()
        
    def get_only_favorite(self):
        self.cursor.execute("SELECT id, text, created, favorite FROM thoughts WHERE favorite = 1 ORDER BY created DESC")
        return self.cursor.fetchall()
        
    def is_favorite(self, thought_id):
        self.cursor.execute("SELECT favorite FROM thoughts WHERE id = ?", (thought_id,))
        result = self.cursor.fetchone()
        return bool(result[0]) if result else False
    
    def add_tag(self, name):
        self.cursor.execute("INSERT OR IGNORE INTO tags(name) VALUES(?)", (name,))
        self.conn.commit()
        
    def assign_tag(self, thought_id, tag_name):
        self.add_tag(tag_name)
        
        self.cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
        
        tag_id = self.cursor.fetchone()[0]
        
        self.cursor.execute("INSERT OR IGNORE INTO thought_tags(thought_id, tag_id) VALUES(?, ?)", (thought_id, tag_id))
        
        self.conn.commit()
        
    def get_tags(self, thought_id):
        self.cursor.execute("SELECT tags.name FROM tags JOIN thought_tags ON tags.id = thought_tags.tag_id WHERE thought_tags.thought_id = ?", (thought_id,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def remove_tag(self, thought_id, tag_name):
        self.cursor.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
        tag_id = self.cursor.fetchone()
        
        if tag_id:
            tag_id = tag_id[0]
            self.cursor.execute("DELETE FROM thought_tags WHERE thought_id = ? AND tag_id = (SELECT id FROM tags WHERE name = ?)", (thought_id, tag_name))
            self.conn.commit()
            
    def search_tag(self, tag):
        self.cursor.execute("""
            SELECT DISTINCT thoughts.id, thoughts.text, thoughts.created, thoughts.favorite
            FROM thoughts
            JOIN thought_tags ON thoughts.id = thought_tags.thought_id
            JOIN tags ON thought_tags.tag_id = tags.id
            WHERE tags.name LIKE ?
            ORDER BY thoughts.created DESC
        """, (f"%{tag}%",))
        
        return self.cursor.fetchall()
    
    def get_tagged_thoughts(self):
        self.cursor.execute("SELECT DISTINCT thoughts.id, thoughts.text, thoughts.created, thoughts.favorite FROM thoughts JOIN thought_tags ON thoughts.id = thought_tags.thought_id ORDER BY thoughts.created DESC")
        return self.cursor.fetchall()
    
    def add_reminder(self, thought_id, reminder_time):
        self.cursor.execute("INSERT INTO reminders (thought_id, reminder_time) VALUES(?, ?)", (thought_id, reminder_time))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_reminder(self, thought_id):
        self.cursor.execute("SELECT id, reminder_time FROM reminders WHERE thought_id = ?", (thought_id,))
        return self.cursor.fetchall()
    
    def delete_reminder(self, reminder_id):
        self.cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        self.conn.commit()
        
    def get_due_reminders(self):
        self.cursor.execute(
            """
            SELECT reminders.id, reminders.thought_id, reminders.reminder_time, thoughts.text 
            FROM reminders
            
            JOIN thoughts ON thoughts.id = reminders.thought_id
            
            WHERE reminders.triggered = 0 and reminders.reminder_time <= datetime('now')
            
            ORDER BY reminders.reminder_time
            """
        )
        
        return self.cursor.fetchall()
    
    def mark_reminder_triggered(self, reminder_id):
        self.cursor.execute("UPDATE reminders SET triggered = 1 WHERE id = ?", (reminder_id,))
        self.conn.commit()
                
    def close(self):
        self.conn.close()