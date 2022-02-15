from .db.sqlite_storage import SQLiteStorage

storage = SQLiteStorage(echo=False)
storage.reload()
