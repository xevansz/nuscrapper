def scrape_novels(pageNo):
    from playwright.sync_api import sync_playwright
    from playwright_stealth import stealth_sync
    import time
    import random
    import re

    def random_delay(min=1, max=4):
        time.sleep(random.uniform(min, max))

    all_novels = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=[
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-extensions",
        "--disable-infobars",
        "--no-sandbox",
    ])
        page = browser.new_page()
        stealth_sync(page)

        url = f"https://www.novelupdates.com/series-finder/?sf=1&org=495,496,497&sort=sdate&order=desc&pg={pageNo}"
        print(f"scraping page {pageNo}")

        try:
            page.goto(url)
            page.wait_for_selector(".search_title")
            random_delay()

            novel_box = page.query_selector_all(".search_body_nu")

            for box in novel_box:
                try:
                    # Title
                    title = title_elem.inner_text().strip() if (title_elem:=box.query_selector(".search_title a")) else "N/A"

                    # Traverse siblings
                    stats_div = box.query_selector(".search_stats")
                    genre_div = box.query_selector(".search_genre")
                    url = url_elem.get_attribute("href") if (url_elem:=box.query_selector(".search_title a")) else "N/A"
                    origin = box.query_selector(".search_ratings .orgcn, .search_ratings .orgkr, .search_ratings .orgjp")
                    rating_span = box.query_selector(".search_ratings")
                    img_div = box.query_selector(".search_img_nu img")

                    # Helper to get stat text
                    def get_stat_text(div, icon_class):
                        icon = div.query_selector(f".{icon_class}")
                        return icon.evaluate('el => el.parentElement.textContent.trim()') if icon else "N/A"

                    cover_url = img_div.get_attribute("src") if img_div else "N/A"
                    chapters = get_stat_text(stats_div, "fa-list-alt")
                    freq = get_stat_text(stats_div, "fa-bolt")
                    readers = get_stat_text(stats_div, "fa-user-o")
                    reviews = get_stat_text(stats_div, "fa-pencil-square-o")
                    updated = get_stat_text(stats_div, "fa-calendar")
                    origin = origin.inner_text().strip() if origin else "N/A"
                    genres = [g.inner_text().strip() for g in genre_div.query_selector_all("a")] if genre_div else []
                    
                    if rating_span:
                        rating_text = rating_span.inner_text().strip()
                        match = re.search(r"\(([\d.]+)\)", rating_text)
                        rating = match.group(1) if match else "N/A"
                    else:
                        rating = "N/A"

                    # desc not working so lets simualte a full click - okay did not work i am missing something but lets skip that i am too lazy
                    # text = desc_div.inner_text().strip()
                    # description = text.split("...more>>")[0].strip() if "...more>>" in text else text
                    description = box.evaluate("""
                         el => {
                            let desc = '';
                            for (let node of el.childNodes) {
                                if (node.nodeType === 3) {
                                    desc += node.textContent;
                                }
                            }
                            return desc.trim();
                        }
                    """)

                    all_novels.append({
                        "Title": title,
                        "Cover": cover_url,
                        "Chapters": chapters,
                        "Update Frequency": freq,
                        "Readers": readers,
                        "Reviews": reviews,
                        "Last Updated": updated,
                        "Genres": genres,
                        "Origin": origin,
                        "Rating": rating,
                        "Description": description,
                        "Source": url
                    })

                    # print(f"✔ {title}")

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
    pageNo = 870

    while True:
        novels = scrape_novels(pageNo)
        if not novels:
            print(f"Stopping at page {pageNo}")
            break

        results.extend(novels)

        try:
            pd.DataFrame(results).to_csv("Novelupdates_info3.csv", index=False, encoding='utf-8', quoting=1)
            print(f"    Page {pageNo} Saveed yooo!!, total so far: {len(results)}")
        except Exception as e:
            print("C'mmon bro not this too: {e}")
        
        pageNo += 1
    
    if results:
        print("🎉 All Done yo, total scraped:", len(results))
    else:
        print("💀 We good? NO NOVELS SCRAPED!!!")
if __name__ == "__main__":
    main()