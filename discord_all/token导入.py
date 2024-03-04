import asyncio
from playwright.async_api import async_playwright
from ads_base.ads_main import AdsAuto
import csv
import threading, time

ads_auto = AdsAuto()  # 创建实例
open_file = r"D:\CODE\python\ADS\ads_base\all_info.csv"


def get_token(key):
    with open(open_file, 'r') as f:
        data = csv.DictReader(f)
        for row in data:
            if row['ads_name'] == f"ads{key}":
                token = row["discord_token"]
                print(token)
                return token


async def change_language(key):
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
            print(f'ads{key}更改语言成功')
            break


async def discord_login(key):
    page = await ads_auto.context.new_page()
    url = "https://discord.com/login"
    i = 0
    while i < 3:
        try:
            await page.goto(url, timeout=100000)
            await page.wait_for_load_state("networkidle")  # 等待页面加载完毕
            print(f'正在登录 ads{key}')
            token = get_token(key)

            if not token:
                print(f"ads{key} 获取token失败")
                break

            print(f'ads{key} token is {token}')
            js_script = f'''
            let token ="{token}";
        function login(token) {{
          setInterval(() => {{
            document.body.appendChild(
              document.createElement`iframe`
            ).contentWindow.localStorage.token = `"${{token}}"`;
          }}, 50);
          setTimeout(() => {{
            location.reload();
          }}, 2500);
        }}
        
        login(token);
        '''
            try:
                print(f'ads{key}开始登录脚本')
                await page.evaluate(js_script)
                await page.wait_for_load_state()  # 等待页面重新加载
                print(f'ads{key}discord token 已使用')
            except Exception as err:
                print(f'Error while running script on ads{key}: {err}')
                print(f'ads{key}discord登录脚本失败')
                break

            await page.wait_for_timeout(3000)

            try:
                await page.wait_for_selector('//button[@aria-label="Закрыть"]', timeout=5000)
                await page.click('//button[@aria-label="Закрыть"]', timeout=5000)
            except Exception as err:
                print(f"Error while closing the popup on ads{key}: {err}")
                print(f"ads{key}进入页面1,无显示")

            try:
                await page.wait_for_selector('//div[@class="contentContainer-qRbgi7"]/button', timeout=5000)
                await page.click('//div[@class="contentContainer-qRbgi7"]/button', timeout=5000)
            except Exception as err:
                print(f"Error while proceeding on ads{key}: {err}")
                print(f"ads{key}进入页面2，无显示")

            print(f"ads{key}登录成功,关闭浏览器")
            await page.wait_for_timeout(5000)
            break
        except Exception as e:
            print(e)
            i += 1
        finally:
            await page.close()
            time.sleep(5)




##开始创建实例

async def run(key) -> None:
    i = 0
    while i<3:
        try:
            async with async_playwright() as playwright:
                await ads_auto.ads_open(playwright, key)
                await discord_login(key)
                break
        except Exception as e:
            print(f'ads{key}失败，重新执行')
            time.sleep(5)



##开始多线程运行程序
def main():
    key_list = list(range(1,10))
    # key_list = [7]  # ads编号

    i = 0
    while i < len(key_list):
        key = key_list[i]

        def threads():
            asyncio.run(run(key))  # dis按照顺序读取

        t = threading.Thread(target=threads)
        t.start()
        # t.join()  # 单线程 ， 注释掉就是多线程
        time.sleep(3)
        i += 1


if __name__ == '__main__':
    main()
