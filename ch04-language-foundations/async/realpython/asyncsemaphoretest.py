import asyncio
import time
import aiohttp


async def download_site(session:aiohttp.ClientSession, url:str, mySemaphore:asyncio.Semaphore):
    await mySemaphore.acquire()
    async with session.get(url) as response:
        print("Read {0} from {1}".format(response.content_length, url))
    mySemaphore.release()

async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        mySemaphore = asyncio.Semaphore(value=10)
        for url in sites:
            task = asyncio.ensure_future(download_site(session, url, mySemaphore))
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()

    # create the loop
    asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")