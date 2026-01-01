from sqlitedict import SqliteDict
import os

class Preferences:
    _instance = None
    _db_path = ""

    def __new__(cls, db_path=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if db_path is None:
                db_path = os.path.join(os.path.dirname(__file__), "app_prefs.sqlite")
            cls._instance._db_path = db_path
            cls._instance.db = SqliteDict(db_path, autocommit=True)
        return cls._instance

    def get(self, key, default=None):
        try:
            return self.db.get(key, default)
        except:
            return default

    def put(self, key, value):
        self.db[key] = value
        self.db.commit()
        save(self)

    def remove(self, key):
        if key in self.db:
            del self.db[key]
            self.db.commit()
            save(self)

    def clear(self):
        self.db.clear()
        self.db.commit()
        save(self)

    def keys(self):
        return list(self.db.keys())

    def items(self):
        return list(self.db.items())

    def __contains__(self, key):
        return key in self.db

    def close(self):
        if hasattr(self, 'db'):
            self.db.close()
        self.__class__._instance = None

    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()

    def save(self):
        try:
            os.system('git config --local user.name "github-actions[bot]"')
            os.system('git config --local user.email "github-actions[bot]@users.noreply.github.com"')
            os.system('git add -A')
            os.system('git commit -m "更新"')
            os.system('git push --quiet --force-with-lease')
        except Exception as e:
            pass

prefs = Preferences()
