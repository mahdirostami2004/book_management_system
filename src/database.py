import os
import sqlite3
from typing import Optional, List, Dict, Any

from src.config import DATABASE_CONFIG


class Database:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DATABASE_CONFIG["db_path"]
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self) -> bool:
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            print(f"خطا در اتصال به پایگاه داده: {e}")
            return False
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")
            return False

    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception as e:
                print(f"خطا در بستن اتصال: {e}")
            finally:
                self.connection = None

    def _ensure_connection(self) -> bool:
        return bool(self.connection) or self.connect()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        if not self._ensure_connection():
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            rows = cursor.fetchall()
            columns = [d[0] for d in cursor.description] if rows else []
            cursor.close()
            return [{col: row[col] for col in columns} for row in rows]
        except sqlite3.Error as e:
            print(f"خطا در اجرای کوئری: {e}")
            print(f"کوئری: {query}")
            if params:
                print(f"پارامترها: {params}")
            return []
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")
            return []

    def execute_update(self, query: str, params: tuple = None) -> bool:
        if not self._ensure_connection():
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            print(f"خطا در اجرای به‌روزرسانی: {e}")
            print(f"کوئری: {query}")
            if params:
                print(f"پارامترها: {params}")
            if self.connection:
                self.connection.rollback()
            return False
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def execute_many(self, query: str, params_list: List[tuple]) -> bool:
        if not self._ensure_connection():
            return False
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, params_list)
            self.connection.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            print(f"خطا در اجرای دسته‌ای: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def test_connection(self) -> bool:
        try:
            if not self._ensure_connection():
                return False
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except Exception:
            return False

    def execute_script(self, script: str) -> bool:
        if not self._ensure_connection():
            return False
        try:
            self.connection.executescript(script)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"خطا در اجرای اسکریپت: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")
            if self.connection:
                self.connection.rollback()
            return False
