import asyncio
import cProfile
import pstats
import re
import time

import httpx
import requests

top_sites = """
https://google.com
https://youtube.com
https://facebook.com
https://amazon.com
https://yahoo.com
https://wikipedia.org
https://zoom.us
https://reddit.com
"""


def count_https_in_web_pages() -> None:
    """before profiling. many actions could impact performance"""

    # is it list comp? if this was from file, would it be because of the file read?
    urls = [url for url in top_sites.split("\n") if url.startswith("https")]

    htmls = []
    for url in urls:
        # is it sync .get?
        htmls += [requests.get(url).text]

    count_https = 0
    count_http = 0
    for html in htmls:
        # is it re.findall, instead of precompiled regex?
        count_https += len(re.findall("https://", html))
        count_http += len(re.findall("http://", html))

    print("finished parsing")
    time.sleep(2)  # someone forgot to remove this
    print(f"{count_http = }")
    print(f"{count_https = }")
    print(f"{count_http / count_https = }")


async def count_https_in_web_pages2() -> None:
    """
    after profiling, identified main sources of time hog:
    time.sleep 2s, and requests.get 9.68s
    solution: remove sleep, make get async
    """
    urls = [url for url in top_sites.split("\n") if url.startswith("https")]

    # rewrote to async, using httpx
    async with httpx.AsyncClient() as client:
        tasks = (client.get(url) for url in urls)
        reqs = await asyncio.gather(*tasks)

    htmls = [req.text for req in reqs]
    # for url in urls:
    #     htmls += [requests.get(url).text]

    count_https = 0
    count_http = 0
    for html in htmls:
        count_https += len(re.findall("https://", html))
        count_http += len(re.findall("http://", html))

    print("finished parsing")
    # removed time.sleep(2)
    print(f"{count_http = }")
    print(f"{count_https = }")
    print(f"{count_http / count_https = }")


def main() -> None:
    with cProfile.Profile() as pr:
        # count_https_in_web_pages()
        asyncio.run(count_https_in_web_pages2())

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()

    # pip install snakeviz
    # after generating the file, from console:
    # snakeviz profiler_dump.prof
    stats.dump_stats(filename="profiler_dump.prof")


if __name__ == "__main__":
    main()
