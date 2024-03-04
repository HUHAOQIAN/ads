import asyncio
import json
import re

from playwright.async_api import async_playwright
from ads_base.ads_main import AdsAuto

import threading, time

ads_auto = AdsAuto()  # 创建实例
'''获取discord邮箱和用户名'''


async def change_language():
    pages = ads_auto.context.pages
    url = "https://discord.com/channels/@me"
    for i in pages:
        if i.url == url:
            page = i
            await page.goto(url)
            await page.mouse.click(100, 100)
            await page.click('//div[@class="container-YkUktl"]/div[2]/button[3]')
            await page.click('//div[@class="side-2ur1Qk"]/div[24]')
            await page.click("text='English, US'")
            await page.close()


async def get_discord_info():
    page = await ads_auto.context.new_page()
    url = "https://discord.com/channels/@me"
    await page.goto(url)
    # user_setter = page.locator('//section[@aria-label="User area"]/div[2]/div[1]')
    # await user_setter.click()
    # if await user_setter.get_attribute("aria-expanded"):
    #     print("yes")
    await page.mouse.click(100, 100)
    await page.click('//div[@class="container-YkUktl"]/div[2]/button[3]')
    username = await page.locator('//div[@class="usernameInnerRow-1-STdK"]').text_content()
    print(username)
    await page.click('//button[@aria-label="Reveal email address"]')
    email = await page.locator('//button[@aria-label="Hide email address"]/parent::span').text_content()
    email = (re.findall("(.*)Hide", email))[0]

    print(type(email))
    print(f'email is {email}')

    await page.wait_for_timeout(2000)
    # await page.close()
    return username, email


##开始创建实例

async def run(key) -> None:
    async with async_playwright() as playwright:
        try:
            print(f'ads{key}启动')

            await ads_auto.ads_open(playwright, key)
            await change_language()
            username, email = await get_discord_info()
            info = {"ads": key, "discord": {"username": username, "email": email}}

            with open("../scritps_all/constants/all_infos.json", "r") as f:
                all_infos = json.load(f)
                # print(all_infos, "all info")
                if info not in all_infos:
                    for i in all_infos:
                        if i["ads"] == key:
                            all_infos.remove(i)
                    all_infos.append(info)
                    all_infos = sorted(all_infos, key=lambda x: x["ads"])  # 按照ads的顺序排列
                    print(all_infos)
                    with open("../scritps_all/constants/all_infos.json", "w") as f:
                        json.dump(all_infos, f)
            time.sleep(5)
        except Exception as err:
            print(err)
        # await ads_auto.ads_close(key)


##开始多线程运行程序
def main():
    # key_list = list(range(23, 24))
    key_list = [51, 56]  # ads编号
    # key_list = [36]
    i = 0
    while i < len(key_list):
        key = key_list[i]

        def threads():
            asyncio.run(run(key))

        t = threading.Thread(target=threads)
        t.start()
        t.join()  # 单线程 ， 注释掉就是多线程
        time.sleep(3)
        i += 1


if __name__ == '__main__':
    main()
