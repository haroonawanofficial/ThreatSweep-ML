import sqlite3

class DatabaseManager:
    def __init__(self, db_file="exploitation_results.db"):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

        # Create a table for storing exploitation results if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS exploitation_results (
                id INTEGER PRIMARY KEY,
                target TEXT,
                service_name TEXT,
                service_version TEXT,
                port INTEGER,
                cve_list TEXT,
                exploitation_result TEXT
            )
        ''')
        self.connection.commit()

    def store_exploitation_result(self, target, service_name, service_version, port, cve_list, exploitation_result):
        # Insert the exploitation result into the database
        self.cursor.execute('''
            INSERT INTO exploitation_results (target, service_name, service_version, port, cve_list, exploitation_result)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (target, service_name, service_version, port, ', '.join(cve_list), exploitation_result))
        self.connection.commit()

    def close(self):
        self.connection.close()
