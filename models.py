import sqlite3
import os

class Task:
    def __init__(self, t_id, title, description, deadline, priority, status):
        self.id = t_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = status

    def to_tuple(self):
        return (self.title, self.description, self.deadline, self.priority, self.status)

class Database:
    """Handles the SQLite connections and CRUD operations for Tasks."""
    def __init__(self, db_name="smart_tasks.db"):
        self.db_name = db_name
        self.conn = self._connect()
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT,
            priority TEXT,
            status TEXT
        )
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def get_all_tasks(self, filter_status=None, filter_priority=None):
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        if filter_status and filter_status != "All":
            query += " AND status = ?"
            params.append(filter_status)
        if filter_priority and filter_priority != "All":
            query += " AND priority = ?"
            params.append(filter_priority)
        
        query += " ORDER BY deadline ASC"
        
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [Task(*row) for row in rows]

    def add_task(self, task):
        query = """
        INSERT INTO tasks (title, description, deadline, priority, status)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.conn.cursor()
        cursor.execute(query, task.to_tuple())
        self.conn.commit()

    def update_task(self, task):
        query = """
        UPDATE tasks
        SET title = ?, description = ?, deadline = ?, priority = ?, status = ?
        WHERE id = ?
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (*task.to_tuple(), task.id))
        self.conn.commit()

    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (task_id,))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
