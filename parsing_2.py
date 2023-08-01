import os
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import Select



os.environ['PATH'] += r"C:\Users\DELL\selenium_drivers\chromedriver_win64"
#hltv = "https://hltv.org"
#chrome_options = Options()
#chrome_options.add_experimental_option("detach", True)
#chrome_options.add_argument("--disable-blink-features")
#chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#chrome_options.add_argument("start-maximized")
#chrome_options.add_argument("--headless")
#chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#chrome_options.add_experimental_option('useAutomationExtension', False)
#chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
#driver = webdriver.Chrome(options=chrome_options)
driver = uc.Chrome()

driver.get("https://hltv.org")
time.sleep(10)

event = "blast fall groups 2023"
#variables for dataset
teams = []
team_rating = []
event_rating = []

search = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "navsearchinput.tt-input.js-bound"))
)
search.click()

search.send_keys(event)
time.sleep(2)
driver.find_element(By.CLASS_NAME,'fa.fa-search').click()
time.sleep(3)
driver.find_element(By.CLASS_NAME,'table').find_element(By.TAG_NAME,'a').click()

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME,'event-hub-link'))
)
driver.find_elements(By.CLASS_NAME,'event-hub-link')[2].click()

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME,'stats-section.stats-team.stats-sidebar'))
)
driver.find_elements(By.CLASS_NAME,'sidebar-single-line-item')[2].click()

table = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME,'stats-table.player-ratings-table'))
)
rows = table.find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr')
num_teams = len(rows)
for index in range(num_teams):
    names = driver.find_element(By.CLASS_NAME,'stats-table.player-ratings-table').find_element(By.TAG_NAME,'tbody').find_elements(By.CLASS_NAME,'teamCol-teams-overview')
    ratings = driver.find_element(By.CLASS_NAME,'stats-table.player-ratings-table').find_element(By.TAG_NAME,'tbody').find_elements(By.CLASS_NAME,'ratingCol')
    
    teams.append(names[index].text)
    team_rating.append(float(ratings[index].text))

    action_chains = ActionChains(driver)
    action_chains.key_down(Keys.CONTROL).click(names[index].find_element(By.TAG_NAME,'a')).key_up(Keys.CONTROL).perform()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the second tab/window (index 1)

    driver.find_elements(By.CLASS_NAME,'stats-top-menu-item.stats-top-menu-item-link')[3].click()
    rats = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME,'stats-table.player-ratings-table'))
    )
    sum=0
    for stat in rats.find_elements(By.CLASS_NAME,'ratingCol')[1:]:
        sum += float(stat.text)
    event_rating.append(sum)

    print(teams)
    print(team_rating)
    print(event_rating)

    driver.close()    
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)



