import json
from database import Database

class Exporter:
    
    @staticmethod
    def export_txt(path, thoughts):
        db = Database()
        
        with open(path, "w", encoding = "utf-8") as file:
            for id, text, date, favorite in thoughts:
                if favorite == 1:
                    file.write("*Favorite Thought*\n\n")
                tags = db.get_tags(id)
                for tag in tags:
                    file.write(f"#{tag} ")
                file.write("\n")
                file.write(f"{date}\n")
                file.write(text + "\n\n")
                file.write("-" * 50)
                file.write("\n\n")
                
    @staticmethod
    def export_markdown(path, thoughts):
        db = Database()
        with open(path, "w", encoding = "utf-8") as file:
            file.write("# ThoughtInbox Export\n\n")
            
            for id, text, date, favorite in thoughts:
                if favorite == 1:
                    file.write("**Favorite Thought**\n\n")
                tags = db.get_tags(id)
                for tag in tags:
                    file.write(f"#{tag} ")
                file.write("\n")
                file.write(f"## {date}\n\n")
                file.write(text)
                file.write("\n\n---\n\n")
                
    @staticmethod
    def export_json(path, thoughts):
        data = []
        db = Database()
        
        for id, text, date, favorite in thoughts:
            tags = db.get_tags(id)
            data.append({"date": date, "thought": text, "favorite": bool(favorite), "tags": tags})
            
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent = 4, ensure_ascii = False)