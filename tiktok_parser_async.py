import time
from datetime import datetime
from os import mkdir, path, devnull

import aiofiles as aiofiles
import asyncio
import aiohttp
from arsenic import get_session
from arsenic.browsers import Chrome
from arsenic.services import Chromedriver


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


async def link_generator(sites_list):
    links = {}
    browser = Chrome(**{"goog:chromeOptions": {'args': ['--headless', '--disable-gpu']}})
    async with get_session(Chromedriver(log_file=devnull), browser) as session:
        for i, site in enumerate(sites_list, start=1):
            try:
                await session.get(site)
                video = await session.wait_for_element(5, "[mediatype = 'video']")
                links[i] = await video.get_attribute("src")
                print(f'Видео {i} - добавлено')
            except:
                print(f'ОШИБКА. Видео по ссылке {i} не добавлено')
                continue
        print(f'\nДобавлено видео: {len(links)}. Сейчас начнётся загрузка видео')
        return links


async def download_video(name, vid_name, link, session):
    try:
        async with aiofiles.open(f'../../Downloaded_videos/{name}/{vid_name}.mp4', 'wb') as file:
            async with session.get(link) as response:
                async for piece in response.content.iter_chunked(2000):
                    await file.write(piece)
            print(f'Файл {vid_name}.mp4 - скачан')
    except:
        print(f'ОШИБКА! Не удалось скачать {vid_name}.mp4')


async def video_downloader(links):
    if not path.exists('../../Downloaded_videos/'):
        mkdir(f'../../Downloaded_videos/')
    name = datetime.now().strftime("%d-%m-%Y - %H.%M.%S")
    mkdir(f'../../Downloaded_videos/{name}')
    async with aiohttp.ClientSession() as session:
        tasks = []
        for vid_name, link in links.items():
            task = asyncio.create_task(download_video(name, vid_name, link, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


sites = sites_getter()
start = time.perf_counter()
links = asyncio.run(link_generator(sites))
asyncio.run(video_downloader(links))
print(f'Готово! Время выполнения: {round(time.perf_counter() - start, 3)} сек')
