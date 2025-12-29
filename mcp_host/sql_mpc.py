import sqlite3

class SQLMCP:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def execute(self, sql: str):
        if not sql.lower().startswith("select"):
            raise ValueError("Solo se permiten consultas SELECT")

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()

        conn.close()
        return [dict(row) for row in rows]
