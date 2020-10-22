from DromParser import get_content, BASE_URL, save_csv, NAME_FILE, get_car_url_list


def main():
    for car_url in get_car_url_list():
        spb_url = car_url.replace('auto.drom.ru', 'spb.drom.ru')
        for content in get_content(spb_url):
            save_csv(NAME_FILE, content)


if __name__ == '__main__':
    main()
