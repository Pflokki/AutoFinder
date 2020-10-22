import urllib.request
import urllib.parse

import csv
import time

from bs4 import BeautifulSoup

import http.client

http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# Insert your URL
BASE_URL = 'https://spb.drom.ru/auto/used/all/?maxprice=250000&transmission=2&inomarka=1&pts=2&unsold=1'
# Insert your NAME File
NAME_FILE = f'[{time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())}] Cars'


def get_html(url):
    try:
        content_page = urllib.request.urlopen(url).read().decode('windows-1251')
        return content_page
    except http.client.IncompleteRead:
        return False


def parse_html(list_object):
    list_cars = []

    for car in list_object.find_all('a', {'data-ftid': 'bulls-list_bull'}):
        list_cars.append(car)

    var = []
    description_value = [
        'engine_capacity',
        'fuel_type',
        'transmission',
        'drive_unit',
        'mileage',
    ]

    for car in list_cars:
        car_description = []
        for item in car.find_all('span', {'data-ftid': 'bull_description-item'}):
            car_description.append(item.text.rstrip(','))

        car_description = dict(zip(description_value, car_description))
        # img = next(car.find_all("div", {'data-ftid': 'bull_image'})[0].next_siblings).previous.attrs['src']
        img_div = car.find_all("div", {'data-ftid': 'bull_image'})
        car_image_url = ''
        for img_div_tag in img_div:
            images = img_div_tag.find_all('img')
            if len(images):
                car_image_url = images[0]['data-src']

        car_title = car.find_all("span", {'data-ftid': 'bull_title'})[0].text
        p_car_title = car.find_all("span", {'data-ftid': 'bull_title'})[0].parent.parent
        sub_title_car_title = p_car_title.contents[2].text if len(p_car_title.contents) > 2 else None

        car_date = car.find_all("div", {'data-ftid': 'bull_date'})[0].text

        car_price = car.find_all('span', {'data-ftid': 'bull_price'})[0].text

        car_city = car.find_all('span', {'data-ftid': 'bull_location'})[0].text

        var.append(
            {"url": car['href'],
             "image": car_image_url,
             "title": car_title.split(',')[0],
             "year": car_title.split(',')[1],
             "sub_title": sub_title_car_title,
             "description": car_description,
             "date": car_date,
             "price": car_price,
             "city": car_city,
             }
            )

    print(var)
    return var


def get_car_url_list():
    current_link = "https://spb.drom.ru/"

    contents = []
    content_page = get_html(current_link)
    list_object = BeautifulSoup(content_page, 'html.parser')

    url_list = []
    for url in list_object.find("div", {"class": "footer-sitemap__links-column", "style": "order: 2"}).contents:
        if url.name == 'div':
            for a_tag in url.contents:
                if a_tag.name == 'a':
                    url_list.append(a_tag['href'])

    # car_url_list = []
    for group_car_url in url_list:
        content_page = get_html(group_car_url)
        list_object = BeautifulSoup(content_page, 'html.parser')
        urls = list_object.find("div", {"class": "sitemap"})
        for car_url in urls.contents:
            if car_url.name == 'p':
                yield car_url.contents[0]['href']

    # return parse_html(list_object)


def save_csv(namefile, data):
    if len(data):
        with open(f"{namefile}.csv", "a", encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, data[0].keys())
            for car in data:
                csv_writer.writerow(car)


def get_content(current_link, delay=False):
    count = 1

    while current_link is not None:
        print(("Pages: {0}".format(count)))
        time.sleep(1)

        if delay:
            if count % 10 == 0:
                time.sleep(30)
            elif count % 5 == 0:
                time.sleep(15)

        contents = []
        content_page = get_html(current_link)
        list_object = BeautifulSoup(content_page, 'html.parser')

        next_page_element = list_object.find("a", {"data-ftid": "component_pagination-item-next"})
        current_link = next_page_element['href'] \
            if next_page_element is not None and 'href' in next_page_element.attrs else None
        count += 1

        yield parse_html(list_object)
