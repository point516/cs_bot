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
#driver.find_element(By.ID,'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll').click()
event = "blast fall groups 2023"

#variables for dataset        #should be updated each iteration
team_names = []
maps = []
y_true = []

winstreak = [0.0,0.0]
h2h = [0,0]
ranking = [0,0]
weeks = [0,0]
age = [0,0]
map_winrate = []
maps_played = []
_5v4 = []
_4v5 = []
pistol = []
rating_3m = []

search = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "navsearchinput.tt-input.js-bound"))
)
search.click()

search.send_keys(event)
time.sleep(2)
driver.find_element(By.CLASS_NAME,'fa.fa-search').click()
time.sleep(3)
driver.find_element(By.CLASS_NAME,'table').find_element(By.TAG_NAME,'a').click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME,'event-hub-link'))
)
driver.find_elements(By.CLASS_NAME,'event-hub-link')[1].click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME,'result'))
)
num = len(driver.find_elements(By.CLASS_NAME,'result'))
#winstreaks
for match_order in range(num):
    #need to go to results page?
    matches = driver.find_elements(By.CLASS_NAME,'result')

    action_chains = ActionChains(driver)
    action_chains.key_down(Keys.CONTROL).click(matches[match_order]).key_up(Keys.CONTROL).perform()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the second tab/window (index 1)


    team_names.append(driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[0].text)
    team_names.append(driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[1].text)


    past_matches = driver.find_elements(By.CLASS_NAME,'past-matches-box.text-ellipsis')   
    for i, box in enumerate(past_matches):
        try:
            streak = box.find_element(By.CLASS_NAME,'past-matches-streak')
        except:
            continue
        else:
            winstreak[i] = float(streak.text[0])

    #H2h
    h2h[0] = float(driver.find_element(By.CLASS_NAME,'flexbox-column.flexbox-center.grow.right-border').find_element(By.CLASS_NAME,'bold').text)
    h2h[1] = float(driver.find_element(By.CLASS_NAME,'flexbox-column.flexbox-center.grow.left-border').find_element(By.CLASS_NAME,'bold').text)


    for map in driver.find_elements(By.CLASS_NAME,'mapholder'):
        try:
            maps.append(map.find_element(By.CLASS_NAME,'played').find_element(By.TAG_NAME,'img').get_attribute('title'))
            y_true.append(float(team_names.index(map.find_element(By.CLASS_NAME,'results.played').find_element(By.CLASS_NAME,'won').find_element(By.TAG_NAME,'img').get_attribute('title'))))
        except:
            continue

    for team in range(2):
        action_chains = ActionChains(driver)
        action_chains.key_down(Keys.CONTROL).click(driver.find_elements(By.CLASS_NAME,'team')[team]).key_up(Keys.CONTROL).perform()
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the second tab/window (index 1)

        stats = driver.find_elements(By.CLASS_NAME,'profile-team-stat')

        ranking[team] = float(stats[0].find_element(By.CLASS_NAME,'right').text[1:])
        weeks[team] = float(stats[1].find_element(By.CLASS_NAME,'right').text)  
        age[team] = float(stats[2].find_element(By.CLASS_NAME,'right').text)

        driver.find_elements(By.CLASS_NAME,'tab.text-ellipsis')[-1].click()
        for map in driver.find_elements(By.CLASS_NAME,'map-statistics-row'):
            if map.find_element(By.CLASS_NAME,'map-statistics-row-map-mapname').text in maps:
                map_winrate.append(float(map.find_element(By.CLASS_NAME,'map-statistics-row-win-percentage').text[:-1])/100)
                map.click()

                time.sleep(1)
                stats = driver.find_element(By.CLASS_NAME,'map-statistics-extended.active')

                maps_played.append(float(stats.find_elements(By.CLASS_NAME,'stat')[0].text) + float(stats.find_elements(By.CLASS_NAME,'stat')[2].text))
                _5v4.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[0].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)
                _4v5.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[1].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)
                pistol.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[2].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)

                driver.find_element(By.CLASS_NAME,'map-statistics-row.active').click()

        driver.find_elements(By.CLASS_NAME,'moreButton')[-1].click()
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME,'stats-top-menu-item.stats-top-menu-item-link'))
        )

        driver.find_elements(By.CLASS_NAME,'stats-top-menu-item.stats-top-menu-item-link')[3].click()
        Select(driver.find_element(By.CLASS_NAME,'stats-sub-navigation-simple-filter-time')).select_by_index(2)
        time.sleep(2)
        sum=0
        for stat in driver.find_element(By.CLASS_NAME,'stats-table.player-ratings-table').find_elements(By.CLASS_NAME,'ratingCol')[1:]:
            sum += float(stat.text)
        rating_3m.append(sum)

        driver.close()
        driver.switch_to.window(driver.window_handles[1])  # Switch to the first tab at the end of parsing first team

        print(team_names)
        print(y_true)
        print(maps)
        print(winstreak)
        print(h2h)
        print(ranking)
        print(weeks)
        print(age)
        print(map_winrate)
        print(maps_played)
        print(_5v4)
        print(_4v5)
        print(pistol)
        print(rating_3m)



        time.sleep(5)
    
    driver.close()    
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)


driver.quit()