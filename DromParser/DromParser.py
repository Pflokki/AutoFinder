import csv
import time

from bs4 import BeautifulSoup

from aiohttp import ClientSession

from DromParser.payload.HTMLCarParser import HTMLCarParser

# Insert your URL
BASE_URL = 'https://spb.drom.ru/auto/used/all/?maxprice=250000&transmission=2&inomarka=1&pts=2&unsold=1'
# Insert your NAME File
NAME_FILE = f'[{time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())}] Cars'


session = ClientSession()


async def get_html(url, session: ClientSession):
    content = await session.get(url)
    return await content.text()


async def get_start_page_content():
    current_link = "https://spb.drom.ru/"

    content_page = await get_html(current_link, session)
    list_object = BeautifulSoup(content_page, 'html.parser')
    return list_object.find("div", {"class": "footer-sitemap__links-column", "style": "order: 2"}).contents


async def get_group_car_url():
    url_list = await get_start_page_content()
    for url in url_list:
        if hasattr(url, 'name') and url.name == 'div':
            for a_tag in url.contents:
                if a_tag.name == 'a':
                    yield a_tag['href']


async def get_car_url():
    async for group_car_url in get_group_car_url():
        content_page = await get_html(group_car_url, session)
        list_object = BeautifulSoup(content_page, 'html.parser')
        urls = list_object.find("div", {"class": "sitemap"})
        for car_url in urls.contents:
            if car_url.name == 'p':
                yield car_url.contents[0]['href']


def save_csv(namefile, data):
    if len(data):
        with open(f"{namefile}.csv", "a", encoding='utf-8') as csv_file:
            print(f"added {len(data)} cars, from {data[0].title} to {data[-1].title}")
            csv_writer = csv.DictWriter(csv_file, data[0].to_dict().keys())
            for car in data:
                csv_writer.writerow(car.to_dict())


async def get_content(current_link, delay=False):
    count = 1

    while current_link is not None:
        content_page = await get_html(current_link, session)
        list_object = BeautifulSoup(content_page, 'html.parser')
        parser = HTMLCarParser()
        await parser.parse(list_object)
        car_list = parser.get_car_list()

        next_page_element = list_object.find("a", {"data-ftid": "component_pagination-item-next"})
        current_link = next_page_element['href'] \
            if next_page_element is not None and 'href' in next_page_element.attrs else None
        count += 1

        yield car_list
