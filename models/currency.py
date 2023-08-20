# Descrição:
# Este arquivo Python ilustra como estabelecer uma conexão com um banco de dados SQLite e
# realizar operações básicas de criação de tabelas, inserção de dados e consultas. O código define uma
# classe chamada "Currency" que encapsula as operações relacionadas à tabela "currency" em um banco de
# dados chamado "cryptoCurrency.sqlite".

import sqlite3


class Currency:
    def __init__(self):
        self.table_name = 'currency'
        self.conn = sqlite3.connect('cryptoCurrency.sqlite')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                date DATE PRIMARY KEY,
                id INTEGER NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL
            );
        """)

    def drop_table(self):
        self.cursor.execute(f"""
            DROP TABLE IF EXISTS {self.table_name};
        """)

    def insert(self, item):
        self.cursor.execute(f"""
            INSERT OR REPLACE INTO {self.table_name}
            VALUES (?, ?, ?, ?);
        """, item)
        self.conn.commit()

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

    def read_one(self, date):
        self.cursor.execute(f"""
            SELECT * FROM {self.table_name} WHERE date = '{date}';
        """)
        return self.cursor.fetchone()


if __name__ == '__main__':
    # Execute este arquivo para criar o banco de dados e a tabela
    db = Currency()

    db.drop_table()
    db.create_table()

    items = [
        ('2021-01-01', 1, 'Bitcoin', 10000.00),
        ('2021-01-02', 1, 'Bitcoin', 20000.00),
        ('2021-01-03', 1, 'Bitcoin', 30000.00),
        ('2021-01-04', 1, 'Bitcoin', 40000.00),
        ('2021-01-05', 1, 'Bitcoin', 50000.00),
        ('2021-01-06', 1, 'Bitcoin', 60000.00),
    ]

    for item in items:
        db.insert(item)

    print(db.read_all())
