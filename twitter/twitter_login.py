import asyncio
import csv
import sys
from playwright.async_api import async_playwright
from ads_base.ads_main import AdsAuto
import threading, time

ads_auto = AdsAuto()  # 创建实例


def get_twitter_data(key):
    with open(r"D:\CODE\python\ADS\ads_base\all_info.csv", 'r') as f:
        data = csv.DictReader(f)
        for row in data:
            if row['ads_name'] == f"ads{key}":
                username = row["twitter_username"]
                password = row["twitter_password"]
                twitter_mail = row["twitter_mail"]
                twitter_phone = row["twitter_phone"]
                print(username, password, twitter_mail)
                return username, password, twitter_mail,twitter_phone


async def twitter_login(key):
    username, password, mail,phone = get_twitter_data(key)
    print(f'ads{key}正在登录twitter,username is {username}')
    i = 0
    while i < 3:

        page = await ads_auto.context.new_page()
        url = "https://twitter.com/login/"
        try:
            await page.goto(url,timeout=50000)
            await page.wait_for_timeout(2000)
            await page.fill('//input[@autocomplete="username"]', username)
            await page.click('//span[contains(text(),"Next")]')
            await page.fill('//input[@autocomplete="current-password"]', password)
            await page.click('//span[contains(text(),"Log in")]')
            try:
                await page.fill('//input[@autocomplete="tel"]', phone,timeout=5000)
                await page.click('//span[contains(text(),"Next")]')
            except:
                print(f'ads{key}不需要电话')
            try:
                await page.fill('//input[@autocomplete="email"]', mail,timeout=5000)
                await page.click('//span[contains(text(),"Next")]')
            except:
                print(f'ads{key}不需要邮箱')
            print(f'ads{key}登录成功，正在关闭浏览器')
            await page.wait_for_timeout(300000)
            await ads_auto.ads_close(key)
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
                await  twitter_login(key)
            break
        except Exception as e:
            print(e)
            time.sleep(3)
        i += 1


##开始多线程运行程序
def main():
    # key_list = list(range(8,51))
        # key_list = list(range(80,150))
    key_list = [21,39,57,58,59]  # ads编号

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
