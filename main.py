from app.scraper import Scraper
import asyncio


async def main():
    scraper = Scraper(coin_id=1, date_start='2021-01-01', date_end='2021-01-31', interval='1d', convert='BRL')
    results = await scraper.scrap_historical()
    # await scraper.close()
    print(results)

if __name__ == '__main__':
    asyncio.run(main())
