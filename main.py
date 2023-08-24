from app.scraper import Scraper
from database.models import HistoricalOHLC
import asyncio
import argparse


async def parse_args():
    parser = argparse.ArgumentParser(description='Scraper de dados do CoinMarketCap')
    parser.add_argument('-id', '--coin-id', type=int, help='Coin ID do CoinMarketCap')
    parser.add_argument('-start', '--date-start', type=str, help='Data de inicio da extração')
    parser.add_argument('-end', '--date-end', type=str, help='Data de fim da extração')
    parser.add_argument('-i', '--interval', type=str, help='Frequencia de extração (1d, 1h, 1m)')
    parser.add_argument('-c', '--convert', type=str, help='Moeda de conversão (BRL, USD, EUR)')
    return parser.parse_args()


async def main():
    args = await parse_args()
    scraper = Scraper(
        coin_id=args.coin_id,
        date_start=args.date_start,
        date_end=args.date_end,
        interval=args.interval,
        convert=args.convert)
    results = await scraper.scrap_historical()

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
