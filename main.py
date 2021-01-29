from DromParser.DromParser import get_car_url, get_content, save_csv, NAME_FILE

import asyncio


async def run():
    async for car_url in get_car_url():
        spb_url = car_url.replace('auto.drom.ru', 'spb.drom.ru')
        async for content in get_content(spb_url):
            save_csv(NAME_FILE, content)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())
