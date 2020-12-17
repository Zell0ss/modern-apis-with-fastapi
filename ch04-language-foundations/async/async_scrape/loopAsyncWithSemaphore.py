import asyncio
import datetime

import bs4
import httpx
import requests
from colorama import Fore

# Older versions of python require calling loop.create_task() rather than asyncio.ensure_future.
# Make this available more easily.
global loop



async def get_html(episode_number: int, mySemaphore:asyncio.Semaphore) -> str:
    print(Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True)

    url = f'https://talkpython.fm/{episode_number}'
    
    await mySemaphore.acquire()
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
    mySemaphore.release()
    return resp.text


def get_title(html: str, episode_number: int) -> str:
    print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    header = soup.select_one('h1')
    if not header:
        return "MISSING"

    return header.text.strip()


async def get_title_range():
    # Please keep this range pretty small to not DDoS my site. ;)

    tasks = []
    mySemaphore = asyncio.Semaphore(value=3)
    for n in range(270, 280):
        tasks.append((n, loop.create_task(get_html(n, mySemaphore))))
    
    for n, t in tasks:
        html = await t
        title = get_title(html, n)
        print(Fore.WHITE + f"Title found: {title}", flush=True)

def main():
    t0 = datetime.datetime.now()

    global loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_title_range())

    dt = datetime.datetime.now() - t0
    print(f"Done in {dt.total_seconds():.2f} sec.")

if __name__ == '__main__':
    main()
