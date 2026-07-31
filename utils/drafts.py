from pathlib import Path

DRAFT_FILE = Path("data/drafts.txt")

DRAFT_FILE.parent.mkdir(exist_ok = True)

class DraftManager:
    
    @staticmethod
    def save(text):
        with open(DRAFT_FILE, "w", encoding = "utf-8") as f:
            f.write(text)
            
            
    @staticmethod
    def load():
        if not DRAFT_FILE.exists():
            return ""

        with open(DRAFT_FILE, "r", encoding = "utf-8") as f:
            return f.read()
        
    @staticmethod
    def clear():
        if DRAFT_FILE.exists():
            DRAFT_FILE.unlink()
            
            