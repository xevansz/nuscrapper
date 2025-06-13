def scrape_novels(pageNo):
    from playwright.sync_api import sync_playwright
    from playwright_stealth import stealth_sync
    import time
    import random

    def random_delay(min=1, max=4):
        time.sleep(random.uniform(min, max))

    all_novels = []

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

            titles = page.query_selector_all(".search_body_nu .search_title")

            for title_div in titles:
                try:
                    # Title
                    title = title_div.query_selector("a").inner_text().strip() if title_div.query_selector("a") else "N/A"

                    # Traverse siblings
                    stats_div = title_div.evaluate_handle("el => el.nextElementSibling").as_element()
                    genre_div = stats_div.evaluate_handle("el => el.nextElementSibling").as_element()
                    desc_div = genre_div.evaluate_handle("el => el.nextElementSibling").as_element()

                    # Helper to get stat text
                    def get_stat_text(div, icon_class):
                        icon = div.query_selector(f".{icon_class}")
                        return icon.evaluate('el => el.parentElement.textContent.trim()') if icon else "N/A"

                    chapters = get_stat_text(stats_div, "fa-list-alt")
                    freq = get_stat_text(stats_div, "fa-bolt")
                    readers = get_stat_text(stats_div, "fa-user-o")
                    reviews = get_stat_text(stats_div, "fa-pencil-square-o")
                    updated = get_stat_text(stats_div, "fa-calendar")

                    genres = [g.inner_text().strip() for g in genre_div.query_selector_all("a")]

                    # desc not working so lets simualte a full click - okay did not work i am missing something but lets skip that i am too lazy
                    text = desc_div.inner_text().strip()
                    description = text.split("...more>>")[0].strip() if "...more>>" in text else text

                    all_novels.append({
                        "Title": title,
                        "Chapters": chapters,
                        "Update Frequency": freq,
                        "Readers": readers,
                        "Reviews": reviews,
                        "Last Updated": updated,
                        "Genres": genres,
                        "Description": description
                    })

                    print(f"✔ {title}")

                except Exception as e:
                    print(f"⚠ Error scraping novel: {e}")
                    continue

        except Exception as e:
            print(f"Bro, really (•̀⤙•́ )?\n{pageNo}: {e}")
            return []

        browser.close()
        return all_novels

# driver code
def main():
    import pandas as pd
    results = []
    pageNo = 1

    while pageNo<=1:
        novels = scrape_novels(pageNo)
        if not novels:
            print(f"Stopping at page {pageNo}")
            break
        results.extend(novels)
        print(f" Page {pageNo} done, total so far: {len(results)}")
        pageNo += 1
    
    if results:
        try:
            # pd.DataFrame(results).to_csv("Novelupdates_info.csv", index=False)

            # pd.DataFrame(results).to_csv("Novelupdates_info.csv", index=False, encoding='utf-8')

            pd.DataFrame(results).to_csv("Novelupdates_info.csv", index=False, encoding='utf-8', quoting=1)
            print("Succesfully saved yo!!")
        except Exception as e:
            print("C'mmon bro not this too: {e}")
    else:
        print("we good? NO!!!")

if __name__ == "__main__":
    main()