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

betting_page = "https://www.hltv.org/betting/analytics/2365562/heroic-vs-astralis-iem-cologne-2023"
driver.get(betting_page)
time.sleep(10)

#variables
team_names = []
maps = ['Mirage','Inferno','Nuke','Overpass','Vertigo','Ancient','Anubis']
rounds_lost = [] #here firstly stats for one team, then for another
rounds_won = [] #here firstly stats for one team, then for another
first_pick = [] #here one for one team, second for another, ....
first_pick_pc = [] #here one for one team, second for another, ....

team_names.append(driver.find_element(By.CLASS_NAME,'head-to-head-section').find_elements(By.CLASS_NAME,'analytics-team-header')[0].find_element(By.CLASS_NAME,'team-name').text)
team_names.append(driver.find_element(By.CLASS_NAME,'head-to-head-section').find_elements(By.CLASS_NAME,'analytics-team-header')[1].find_element(By.CLASS_NAME,'team-name').text)

map_holder = driver.find_element(By.CLASS_NAME,'analytics-handicap-map-wrapper.g-grid')
for team_stats in map_holder.find_elements(By.CLASS_NAME,'col-6'):
    for map in team_stats.find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr'):
        lost = map.find_elements(By.CLASS_NAME,'analytics-handicap-map-data-avg')[0].text
        won = map.find_elements(By.CLASS_NAME,'analytics-handicap-map-data-avg')[1].text
        if lost != '-':
            rounds_lost.append(float(lost))
            rounds_won.append(float(won))
        else:
            rounds_lost.append(0.0)
            rounds_won.append(0.0)

veto_stats = driver.find_element(By.CLASS_NAME,'analytics-map-stats').find_element(By.TAG_NAME,'tbody')
for row in veto_stats.find_elements(By.TAG_NAME,'tr'):
    first_pick_pc.append(float(row.find_element(By.CLASS_NAME,'analytics-map-stats-pick-percentage').text[:-1])/100)

    try:
        if row.find_element(By.CLASS_NAME,'analytics-map-stats-comment').find_element(By.CLASS_NAME,'comment.neutral').text == 'First pick':
            first_pick.append(True)
        else:
            first_pick.append(False)
    except:
        first_pick.append(False)
        continue

print(team_names)
print(rounds_lost)
print(rounds_won)
print(first_pick)
print(first_pick_pc)