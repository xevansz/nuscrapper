from selenium import webdriver # allow launching browser
from selenium.webdriver.common.by import By # allow search with parameters
from selenium.webdriver.support.ui import WebDriverWait # allow waiting for page to load
from selenium.webdriver.support import expected_conditions as EC # determine whether the web page has loaded
from selenium.common.exceptions import TimeoutException # handling timeout situation

# to open new window
# driver_option = webdriver.ChromeOptions()
# driver_option.add_argument(" — incognito")
# chromedriver_path = '/usr/bin/chromedriver' # Change this to your own chromedriver path!
# def create_webdriver():
#  return webdriver.Chrome(executable_path=chromedriver_path, chrome_options=driver_option)

 # Open the website
browser = webdriver.Chrome()
browser.get("https://www.novelupdates.com/series-finder/?sf=1&org=495,496,497&sort=sdate&order=desc")

# Extract all novels
novels = browser.find_elements_by_xpath("/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[1]/a")

# Extract titles for each novel
novel_list = []
for novel in novels:
 novel_name = novel.text # novel name
 novel_list.append(novel_name)

# Close connection
browser.quit()

# Saving data
title_df = pd.DataFrame.from_dict(novel_list, orient = 'index')
title_df.columns = ['novel_name']
title_df = title_df.reset_index(drop=True)

# /html/body/div[1]/div[2]/div/div/div[1]/table[1]/tbody/tr[2]/td[1]/a

# /html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[4]/div[2]/div[1]/a