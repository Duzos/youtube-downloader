# SOURCE : https://gist.github.com/lanfon72/7284f83552eb871220804f8ee850fe0e
# Thanks to lanfon72 for making this
import asyncio
from datetime import datetime
from functools import partial
from concurrent.futures import ProcessPoolExecutor

from youtube_dl import YoutubeDL as YDL

PPE = ProcessPoolExecutor()


def extract_info(url, quiet=False):
    # use `quiet=True` to avoid noisy
    return YDL(dict(quiet=quiet)).extract_info(url, download=False)


async def flatten_urls(*urls, loop=None):
    print(f"trying to flat {len(urls)} URLs.")
    loop = asyncio.get_event_loop()
    futs = [loop.run_in_executor(PPE, extract_info, url) for url in urls]
    infos = await asyncio.gather(*futs)

    urlmatrix = [i.get('entries', [i]) for i in infos]
    return [u.get('webpage_url', "") for urls in urlmatrix for u in urls]


async def progress(*urls, loop=None):
    loop = loop or asyncio.get_event_loop()
    print(f"{len(urls)} URLs will be progress.")
    pure_urls = await flatten_urls(*urls, loop=loop)
    print(pure_urls)
    futs = [loop.run_in_executor(None, YDL().download, [url]) for url in pure_urls]
    return await asyncio.gather(*futs)


async def keep_noise():
    while True:
        await asyncio.sleep(1)
        print(f"Time is: {datetime.now()}", flush=True)


def main():
    u1 = ["https://youtu.be/-JNeBKlG0cI",
          "https://youtu.be/mVEItYOsXjM",
          "https://youtu.be/0JoMqP5UwQ8"]
    u2 = ["https://youtu.be/m3gLNa-fx_w"]
    u3 = ["https://www.youtube.com/watch?v=sm4BID47dTI&list=PLFWyAXHl5a6ffjKkNGu27BEk1US055MzB"]
    loop = asyncio.get_event_loop()

    coros = [progress(*u1), progress(*u2), progress(*u3), keep_noise()]
    loop.run_until_complete(asyncio.gather(*coros))


if __name__ == '__main__':
    main()