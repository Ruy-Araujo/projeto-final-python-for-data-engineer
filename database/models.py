# Descrição:
# Este arquivo Python ilustra como estabelecer uma conexão com um banco de dados SQLite e
# realizar operações básicas de criação de tabelas, inserção de dados e consultas. O código define uma
# classe chamada "Currency" que encapsula as operações relacionadas à tabela "currency" em um banco de
# dados chamado "cryptoCurrency.sqlite".

import sqlite3
from datetime import datetime

db_name = 'coin_cap.sqlite'


class AbstractModel():
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def drop_table(self):
        self.cursor.execute(f"""
            DROP TABLE IF EXISTS {self.table_name};
        """)

    def read_all(self):
        self.cursor.execute(f"""
            SELECT * FROM {self.table_name};
        """)
        return self.cursor.fetchall()

    def read_many(self, limit):
        self.cursor.execute(f"""
            SELECT * FROM {self.table_name} LIMIT {limit};
        """)
        return self.cursor.fetchall()

    def read_one(self, id):
        self.cursor.execute(f"""
            SELECT * FROM {self.table_name} WHERE id = {id};
        """)
        return self.cursor.fetchone()


class Assets(AbstractModel):
    def __init__(self):
        super().__init__(table_name='assets')

    def create_table(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL UNIQUE,
                symbol VARCHAR(5) NOT NULL,
                insert_at TIMESTAMP
            );
        """)

    def insert(self, item):
        self.cursor.execute(f"""
            INSERT OR REPLACE INTO {self.table_name}
            VALUES (null, ?, ?, '{datetime.now()}');
        """, item)
        self.conn.commit()


class AssetsHistory(AbstractModel):
    def __init__(self):
        super().__init__(table_name='assets_history')

    def create_table(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                price REAL NOT NULL,
                asset_id INTEGER NOT NULL,
                insert_at TIMESTAMP,
                FOREIGN KEY (asset_id) REFERENCES assets (id)
            );
        """)

    def insert(self, item):
        self.cursor.execute(f"""
            INSERT OR REPLACE INTO {self.table_name}
            VALUES (null, ?, ?, ?, '{datetime.now()}');
        """, item)
        self.conn.commit()


if __name__ == '__main__':
    # Execute este arquivo para criar o banco de dados e a tabela
    assets = Assets()
    assets.drop_table()
    assets.create_table()
    items = [
        ('Bitcoin', 'BTC'),
        ('Ethereum', 'ETH'),
        ('Tether', 'USDT'),
    ]

    for item in items:
        assets.insert(item)

    print(assets.read_all())

    assets_history = AssetsHistory()
    assets_history.drop_table()
    assets_history.create_table()
    items = [
        ('2021-01-01', 1000, 1),
        ('2021-01-02', 2000, 1),
        ('2021-01-03', 3000, 1),
        ('2021-01-01', 100, 2),
        ('2021-01-02', 200, 2),
        ('2021-01-03', 300, 2),
        ('2021-01-01', 1, 3),
        ('2021-01-02', 2, 3),
        ('2021-01-03', 3, 3),
    ]

    for item in items:
        assets_history.insert(item)
    print(assets_history.read_all())
