# -- coding: utf-8 --**
import asyncio
import json, requests, sys,os
from playwright.async_api import Playwright, async_playwright, expect

class AdsAuto:

    async def ads_open(self, playwright: Playwright, key) :
        print("start")
        self.open_url = "http://127.0.0.1:50325/api/v1/browser/start?serial_number=" + str(key)
        self.res = requests.get(self.open_url,proxies={"http":None,"https":None}).json()
        print(self.res)
        if self.res["code"] != 0:
            print(self.res["msg"])
            print("please check ads_id")
            sys.exit()
        # self.res = AdsAuto.ads_requtest(key)
        self.ws_url = self.res["data"]["ws"]["puppeteer"]
        self.browser = await  playwright.chromium.connect_over_cdp(self.ws_url)
        self.context = self.browser.contexts[0]
        # ---------------------
        # await context.close()
        # await browser.close()

    async def ads_close(self,key):
        self.close_url = "http://127.0.0.1:50325/api/v1/browser/stop?serial_number=" + str(key)
        # await self.context.close()
        # await self.browser.close()
        requests.get(self.close_url,proxies={"http":None,"https":None})


    async def ads_check(self, key) -> None:
        self.open_url = ""
        params = {
            # 'user_id' : ''
            'serial_number': str(key)
        }
        check = requests.get(self.check_url, params=params).json()
        print(check)
    async def ads_update(self,key):
        self.update_url= "http://127.0.0.1:50325/api/v1/user/update?"
