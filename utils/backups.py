from pathlib import Path
from shutil import copy2
from datetime import datetime

BACKUP_FOLDER = Path("backups")
DATABASE = Path("thoughts.db")

class BackupManager:
    
    @staticmethod
    def create_backup():
        BACKUP_FOLDER.mkdir(exist_ok = True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup = BACKUP_FOLDER / f"backup_{timestamp}.db"
        copy2(DATABASE, backup)
        BackupManager.cleanup()
        
    @staticmethod
    def cleanup():
        backups = sorted(BACKUP_FOLDER.glob("*.db"), key = lambda p: p.stat().st_mtime, reverse = True)
        
        for old in backups[10:]:
            old.unlink()