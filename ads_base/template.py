import asyncio
from playwright.async_api import async_playwright
from ADS.ads_base.ads_main import AdsAuto

import threading, time

ads_auto = AdsAuto()  # 创建实例


async def sui_form(key):
    i = 0
    while i < 3:

        page = await ads_auto.context.new_page()
        url = "https://accounts.google.com/"
        try:
            await page.goto(url)
            await page.wait_for_timeout(2000)
            break
        except Exception as e:
            print(e)
            time.sleep(3)
            await page.close()
        i += 1


##开始创建实例

async def run(key) -> None:
    i = 0
    while i < 3:
        try:
            async with async_playwright() as playwright:
                await ads_auto.ads_open(playwright, key)
                await ads_auto.ads_close(key)
            break
        except Exception as e:
            print(e)
            time.sleep(3)
        i += 1


##开始多线程运行程序
def main():
    # key_list = list(range(3,39))
    key_list = [4]  # ads编号

    i = 0
    while i < len(key_list):
        key = key_list[i]

        def threads():
            asyncio.run(run(key))

        t = threading.Thread(target=threads)
        t.start()
        # t.join()  # 单线程 ， 注释掉就是多线程
        time.sleep(3)
        i += 1


if __name__ == '__main__':
    main()
