import json

class Exporter:
    
    @staticmethod
    def export_txt(path, thoughts):
        with open(path, "w", encoding = "utf-8") as file:
            for _, text, date, _ in thoughts:
                
                file.write(f"{date}\n")
                file.write(text + "\n\n")
                file.write("-" * 50)
                file.write("\n\n")
                
    @staticmethod
    def export_markdown(path, thoughts):
        with open(path, "w", encoding = "utf-8") as file:
            file.write("# ThoughtInbox Export\n\n")
            
            for _, text, date, _ in thoughts:
                file.write(f"## {date}\n\n")
                file.write(text)
                file.write("\n\n---\n\n")
                
    @staticmethod
    def export_json(path, thoughts):
        data = []
        
        for _, text, date, _ in thoughts:
            data.append({"date": date, "thought": text})
            
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent = 4, ensure_ascii = False)