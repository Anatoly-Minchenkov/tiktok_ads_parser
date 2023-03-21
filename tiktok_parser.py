import time
from datetime import datetime
from os import mkdir, path

from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from requests import get


def sites_getter():
    print('Вставьте ссылки по одной')
    print('Когда закончите - введите "end"')
    sites_list = []

    site_name = input()
    while site_name not in ('end', 'утв'):

        if not (site_name):
            print('У вас пустая ссылка. Введите ещё раз ')
            site_name = input()
            continue
        elif 'http' not in site_name:
            print('Это не ссылка. Введите ещё раз')
            site_name = input()
            continue

        try:
            if str(site_name) not in sites_list:
                sites_list.append(str(site_name))
                print(f'Ссылка {len(sites_list)} добавлена. Введите "end", когда закончите добавлять ссылки')
            else:
                print(f'Вы уже добавляли эту ссылку')
                site_name = input()
                continue
        except:
            print('Что-то пошло не так. Ссылка не добавлена, но можете продолжить загружать ссылки')
            continue
        site_name = input()
    print(f'\nСсылки собраны! Сейчас начнётся сбор видеофайлов. Всего ссылок: {len(sites_list)}.')
    return sites_list


def link_generator(sites_list):
    links = {}
    with uc.Chrome(version_main=110, headless=True) as browser:
        for i, site in enumerate(sites_list, start=1):
            try:
                browser.get(site)
                video = WebDriverWait(browser, 5, poll_frequency=0.5).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'video')))
                links[i] = video.get_attribute("src")
                print(f'Видео {i} - добавлено')
            except:
                print(f'ОШИБКА. Видео по ссылке {i} не добавлено')
                continue
        print(f'\nДобавлено видео: {len(links)}. Сейчас начнётся загрузка видео')
        return links


def vedeo_downloadeer(links):
    if not path.exists('../../Downloaded_videos/'):
        mkdir(f'../../Downloaded_videos/')
    name = datetime.now().strftime("%d-%m-%Y - %H.%M.%S")
    mkdir(f'../../Downloaded_videos/{name}')
    for vid_name, link in links.items():
        response = get(link, stream=True)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            file_path = f'../../Downloaded_videos/{name}/{vid_name}.mp4'
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f'Файл {vid_name}.mp4 - скачан')
        else:
            print(f'ОШИБКА! Файл {vid_name}.mp4 не удалось загрузить')

    print('\nГотово! Можете закрывать программу')


sites = sites_getter()
start = time.perf_counter()
links = link_generator(sites)
vedeo_downloadeer(links)
print(f'Готово! Время выполнения: {round(time.perf_counter() - start, 3)} сек')