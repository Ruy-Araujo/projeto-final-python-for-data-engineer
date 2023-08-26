import asyncio
import logging
import httpx
from tools import to_unixtime_sec, generate_date_ranges


class Scraper:
    BASE_URL = "https://api.coinmarketcap.com/data-api/v3.1"

    def __init__(self, coin_id, date_start, date_end, interval, convert, retry_count=3):
        self.coin_id = coin_id
        self.date_start = date_start
        self.date_end = date_end
        self.interval = interval
        self.convert = convert
        self.retry_count = retry_count
        logging.info(f"Iniciando extrações com os parâmetros: {self.__dict__}")

    async def fetch_historical_data(self, date_start, date_end):
        """
        Obtém os dados históricos de preço das criptomoedas.
        """
        logging.info(f"Iniciando extração de {date_start} até {date_end}...")

        ROUTE = "/cryptocurrency/historical"
        query = {
            "id": self.coin_id,
            "timeStart": await to_unixtime_sec(date_start),
            "timeEnd": await to_unixtime_sec(date_end),
            "interval": self.interval,
            "convert": self.convert,
        }

        for _ in range(self.retry_count):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url=self.BASE_URL + ROUTE, params=query)
                    data = response.json()
                    if data["status"]["error_code"] == "0":
                        logging.info(f"Extração de {date_start} até {date_end} concluída...")
                        return data
                    else:
                        logging.error(f"Erro ao obter dados de {date_start} até {date_end}")
                        logging.error(data["status"]["error_message"])
                        # raise Exception(data["status"]["error_message"])
            except Exception as e:
                logging.error(f"Erro ao obter dados de {date_start} até {date_end}, tentando novamente...")
                await asyncio.sleep(1)

    async def scrap_historical(self):
        """
        Obtém todos os dados históricos de preço das criptomoedas.
        """
        logging.info("Iniciando extração de dados históricos...")
        dates = generate_date_ranges(self.date_start, self.date_end, 30)
        tasks = [self.fetch_historical_data(date[0], date[1]) for date in dates]
        results = await asyncio.gather(*tasks)
        logging.info("Extração de dados históricos concluída...")
        return results

    async def close(self):
        await self.client.aclose()
