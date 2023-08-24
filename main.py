from app.scraper import Scraper
from database.models import HistoricalOHLC
import asyncio


async def main():
    scraper = Scraper(coin_id=1, date_start='2021-01-01', date_end='2021-01-31', interval='1d', convert='BRL')
    results = await scraper.scrap_historical()
    # await scraper.close()

    db = HistoricalOHLC()
    await db.create_table()

    for result in results:
        coin_info = (result['data']['name'], result['data']['symbol'])

        for quote in result['data']['quotes']:
            data = (
                *coin_info,
                quote['quote']['timestamp'][:10],
                quote['quote']['open'],
                quote['quote']['high'],
                quote['quote']['low'],
                quote['quote']['close']
            )

            await db.insert(data)


if __name__ == '__main__':
    asyncio.run(main())
