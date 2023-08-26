# Descrição:
# Este arquivo Python ilustra como estabelecer uma conexão com um banco de dados SQLite e
# realizar operações básicas de criação de tabelas, inserção de dados e consultas. O código define uma
# classe chamada "Currency" que encapsula as operações relacionadas à tabela "currency" em um banco de
# dados chamado "cryptoCurrency.sqlite".
import logging
import sqlite3
from datetime import datetime


db_name = './data/database.sqlite'


class AbstractModel():
    def __init__(self, table_name):
        self.table_name = table_name

    async def execute_query(self, query, parameters=None):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        logging.info(f"Executando query...")
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result

    async def drop_table(self):
        await self.cursor.execute(f"""
            DROP TABLE IF EXISTS {self.table_name};
        """)

    async def read_all(self):
        await self.cursor.execute(f"""
            SELECT * FROM {self.table_name};
        """)
        return self.cursor.fetchall()

    async def read_many(self, limit):
        await self.cursor.execute(f"""
            SELECT * FROM {self.table_name} LIMIT {limit};
        """)
        return self.cursor.fetchall()

    async def read_one(self, id):
        await self.cursor.execute(f"""
            SELECT * FROM {self.table_name} WHERE id = {id};
        """)
        return self.cursor.fetchone()

    async def read_count(self):
        await self.cursor.execute(f"""
            SELECT count(1) registros FROM {self.table_name};
        """)
        return self.cursor.fetchone()


class HistoricalOHLC(AbstractModel):
    def __init__(self):
        super().__init__(table_name='ohlc_historical')

    async def create_table(self):
        logging.info(f"Criando tabela {self.table_name}...")
        await self.execute_query(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                symbol VARCHAR(10) NOT NULL,
                date DATE NOT NULL,
                price_open REAL NOT NULL,
                price_high REAL NOT NULL,
                price_low REAL NOT NULL,
                price_close REAL NOT NULL,
                insert_at TIMESTAMP
            );
        """)

    async def insert(self, item):
        logging.info(f"Inserindo dados na tabela {self.table_name}...")
        await self.execute_query(f"""
            INSERT INTO {self.table_name}
            VALUES (null, ?, ?, ?, ?, ?, ?, ?, '{datetime.now()}');
        """, item)

    async def read_with_filter(self, filter):
        data = await self.execute_query(f"""
            SELECT * FROM {self.table_name} WHERE {filter};
        """)

        return data
