import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import pandas as pd
import random
import time

# told me to delay to make me look human
async def random_delay(page, min=1, max=5):
    delay = random.uniform(min, max)
    await page.wait_for_timeout(delay * 1000)

async def scrapper():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36"
        )
        page = await context.new_page()

        await stealth_async(page)

        url = "https://www.novelupdates.com/series-finder/?sf=1&org=495,496,497&sort=sdate&order=desc"
        print("Opening website")
        await page.goto(url)

        try:
            await page.wait_for_selector(".search_main_box_nu", timeout=10000)
            await random_delay(page)

            novels = await page.query_selector_all(".search_main_box_nu")
            print(f"Found {len(novels)} novels.")

            results = []

            print(novels[:10])
        except Exception as e:
            print(f"Error: {e} probably got found? maybe should use proxy from the start")

asyncio.run(scrapper())