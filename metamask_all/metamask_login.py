import asyncio
from playwright.async_api import async_playwright
from ads_base.ads_main import AdsAuto
import csv
import threading, time
# import pyperclip


ads_auto = AdsAuto()  # 创建实例

def get_mnemonic(key):
    open_file = r'D:\code\python2\ads\ads_base\all_info-pengfei-hu.csv'
    with open(open_file, 'r') as f:
        data = csv.DictReader(f)
        for row in data:
            if row['ads_name'] == f"ads{key}":
                mnemonic = row["wallet_mnemonic"]
    mnemonic = mnemonic.split(" ")
    return mnemonic
async def metamask_login(key):
    page = await ads_auto.context.new_page()
    url = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#"
    mnemonic = get_mnemonic(key)
    print(f'mnemonic is {mnemonic}')

    try:
        await page.goto(url)
        await page.click('//input[@id="onboarding__terms-checkbox"]')
        await page.click('//button[@data-testid="onboarding-import-wallet"]')
        await page.click('//button[@data-testid="metametrics-i-agree"]')
        # await page.click('//button[@data-testid="first-time-flow__button"]', timeout=3000)
        # await page.click('//button[@data-testid="page-container-footer-next"]')
        # await page.click('//button[@data-testid="import-wallet-button"]')
        print('正在输入助记词')
        i = 0
        while i<12:

            await page.fill(f'//input[@id="import-srp__srp-word-{i}"]',mnemonic[i])
            i+=1
        # await page.keyboard.press("Control+V")
        await page.click('//button[@data-testid="import-srp-confirm"]')
        await page.wait_for_timeout(1000)
        await page.fill('//input[@data-testid="create-password-new"]', "QWEqwe123456")
        await page.fill('//input[@data-testid="create-password-confirm"]', "QWEqwe123456")
        await page.click('//input[@data-testid="create-password-terms"]')
        await page.click('//button[@data-testid="create-password-import"]')
        await page.wait_for_timeout(2000)
        try:
            await page.click('//button[@data-testid="onboarding-complete-done"]')
            await page.click('//button[@data-testid="pin-extension-next"]')
            await page.click('//button[@data-testid="pin-extension-done"]')
            print(f'ads{key}登录成功，正在关闭浏览器')
        except:
            pass
        # await page.close()
        # await ads_auto.ads_close(key)
    except Exception as e:
        await page.click('//a[@class="button btn-link unlock-page__link"]')
        await page.wait_for_timeout(1000)
        await page.click('//input[@id="import-srp__srp-word-0"]')
        await page.wait_for_timeout(1000)
        i = 0
        while i < 12:
            await page.fill(f'//input[@id="import-srp__srp-word-{i}"]', mnemonic[i])
            i += 1
        # await page.keyboard.press("Control+V")
        await page.wait_for_timeout(1000)
        await page.fill('//input[@id="password"]', "QWEqwe123456")
        await page.fill('//input[@id="confirm-password"]', "QWEqwe123456")
        await page.click('//button[@type="submit"]')
        await page.wait_for_timeout(2000)
        print(e)
        time.sleep(3)
        await page.close()



##开始创建实例

async def run(key) -> None:
        async with async_playwright() as playwright:
            await ads_auto.ads_open(playwright, key)
            await metamask_login(key)
            await ads_auto.ads_close(key)

##开始多线程运行程序
def main():
    # key_list = list(range(1,150))
    key_list = [151]  # ads编号

    i = 0
    while i < len(key_list):
        key = key_list[i]

        def threads():
            asyncio.run(run(key))

        t = threading.Thread(target=threads)
        t.start()
        t.join()  # 单线程 ， 注释掉就是多线程/
        time.sleep(3)
        i += 1


if __name__ == '__main__':
    main()
