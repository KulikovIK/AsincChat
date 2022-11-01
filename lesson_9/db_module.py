import sqlite3


class MessangerDB:
    def __init__(self):
        self.connection = sqlite3.connect(database='messanger')
        self.cursor = self.connection.cursor()
        self.prepare_base_tables()

    def __del__(self):
        self.connection.close()

    def prepare_base_tables(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INT primary key,
                    login VARCHAR(50) UNIQUE,
                    password VARCHAR(256),
                    info TEXT
                );""")

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients_history (
                    id INT primary key,
                    login_time TIMESTAMP,
                    client_id INT,
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                );""")

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients_contacts (
                    id INT primary key,
                    client_id INT,
                    client_contact INT,
                    FOREIGN KEY (client_id) REFERENCES clients(id),
                    FOREIGN KEY (client_contact) REFERENCES clients(id)
                );""")

    def get_contacts(self, client_id):
        self.cursor.execute("""
                SELECT client_id, client_contact FROM clients_contacts 
                    WHERE client_id=:client""", {'client': client_id})


if __name__ == "__main__":
    db = MessangerDB()
