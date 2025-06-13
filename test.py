from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time
import random
import pandas as pd

def random_delay(min=1, max=4):
    time.sleep(random.uniform(min, max))

all_novels = []

def scrape_novels(pageNo):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        stealth_sync(page)

        url = f"https://www.novelupdates.com/series-finder/?sf=1&org=495,496,497&sort=sdate&order=desc&pg={pageNo}"
        print(f"scraping page {pageNo}")

        try:
            page.goto(url)
            page.wait_for_selector(".search_title")
            random_delay()

            novels = page.query_selector_all(".search_body_nu")
            print(f"Found {len(novels)} novels on {pageNo}")

            for novel in novels:
                titles = novel.query_selector(".search_title").inner_text().strip()
                print(titles)

        except Exception as e:
            print(f"error on page {pageNo}: {e}")
            return False

        browser.close()
        return True

# driver code
def main():
    pageNo = 1
    while pageNo<=2:
        success = scrape_novels(pageNo)
        if not success:
            print(f"Stopping at page {pageNo}")
            break
        pageNo+=1
    print(f"stoping at {pageNo - 1}")

    print("Saving the scraped titles into a csv")
    if all(isinstance(title, str) for title in all_novels):
        df = pd.DataFrame(all_novels, columns=["Title"])
        df.to_csv("Novel_titles.csv")
    else:
        print("Error, some titles are not strings!")

if __name__ == "__main__":
    main()