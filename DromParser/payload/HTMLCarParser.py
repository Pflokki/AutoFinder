from typing import List
from bs4 import BeautifulSoup

from DromParser.payload.Car import Car


class HTMLCarParser:
    def __init__(self):
        self.car_list: List[Car] = []

    def get_car_list(self) -> List[Car]:
        return self.car_list

    async def parse(self, list_object: BeautifulSoup):
        self.car_list.extend([self.get_parsed_car(car)
                              for car in list_object.find_all('a', {'data-ftid': 'bulls-list_bull'})])

    @staticmethod
    def get_parsed_car(car):

        description_value = [
            'engine_capacity',
            'fuel_type',
            'transmission',
            'drive_unit',
            'mileage',
        ]
        car_description = [item.text.rstrip(',')
                           for item in car.find_all('span', {'data-ftid': 'bull_description-item'})]
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

        return Car(
            car['href'],
            car_image_url,
            car_title.split(',')[0],
            sub_title_car_title,
            car_title.split(',')[1],
            car_description,
            car_date,
            car_price,
            car_city
        )
