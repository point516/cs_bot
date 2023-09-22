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
import psycopg2

driver = uc.Chrome()
match = "https://www.hltv.org/matches/2366797/preasy-vs-sharks-cct-2023-online-finals-3"

driver.get(match)
time.sleep(10)

team_names = []
team_rating = [0.95,0.95]
team_names.append(driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[0].text)
team_names.append(driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[1].text)
action_chains = ActionChains(driver)
action_chains.key_down(Keys.CONTROL).click(driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_element(By.CLASS_NAME,'event.text-ellipsis')).key_up(Keys.CONTROL).perform()
time.sleep(5)
driver.switch_to.window(driver.window_handles[-1])
try:
    driver.find_elements(By.CLASS_NAME,'event-hub-link')[3].click()
except:
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)
else:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME,'stats-section.stats-team.stats-sidebar'))
    )
    driver.find_elements(By.CLASS_NAME,'sidebar-single-line-item')[2].click()
    try:
        for item in driver.find_element(By.CLASS_NAME,'stats-table.player-ratings-table').find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr'):
            if item.find_element(By.TAG_NAME,'td').text in team_names:
                team_rating[team_names.index(item.find_element(By.TAG_NAME,'td').text)] = float(item.find_element(By.CLASS_NAME,'ratingCol').text)
    except:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])  # Switch to the first tab at the end of parsing first team
        time.sleep(5)
    else:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)

print(team_rating)
ranking = []
matches_winstreak = []
h2h = []

try:
    ranking.append(float(driver.find_elements(By.CLASS_NAME,"teamRanking")[0].text.split("#")[1]))  
except:
    ranking.append(250.0)

try:
    ranking.append(float(driver.find_elements(By.CLASS_NAME,"teamRanking")[1].text.split("#")[1]))  
except:
    ranking.append(250.0)

h2h.append(float(driver.find_element(By.CLASS_NAME,'flexbox-column.flexbox-center.grow.right-border').find_element(By.CLASS_NAME,'bold').text))
h2h.append(float(driver.find_element(By.CLASS_NAME,'flexbox-column.flexbox-center.grow.left-border').find_element(By.CLASS_NAME,'bold').text))

past_matches = driver.find_elements(By.CLASS_NAME,'past-matches-box.text-ellipsis')[2:]   
for box in past_matches[:2]:
    try:
        streak = box.find_element(By.CLASS_NAME,'past-matches-streak')
    except:
        matches_winstreak.append(0.0)
        continue
    else:
        print(streak.text)
        matches_winstreak.append(float(streak.text[0]))
#####
maps = ['Mirage','Inferno','Nuke','Overpass','Vertigo','Ancient','Anubis']
weeks = []
age = []
_5v4 = []
_4v5 = []
pistol = []
for team in range(2):
    action_chains = ActionChains(driver)
    action_chains.key_down(Keys.CONTROL).click(driver.find_elements(By.CLASS_NAME,'team')[team]).key_up(Keys.CONTROL).perform()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[-1])  # Switch to the second tab/window (index 1)


    stats = driver.find_elements(By.CLASS_NAME,'profile-team-stat')
    weeks.append(float(stats[1].find_element(By.CLASS_NAME,'right').text))
    try:
        age.append(float(stats[2].find_element(By.CLASS_NAME,'right').text))
    except:
        age.append(23.0)


    driver.find_elements(By.CLASS_NAME,'tab.text-ellipsis')[-1].click()
    
    for i in range(len(maps)):
        found = False
        for map in driver.find_elements(By.CLASS_NAME,'map-statistics-row'):
            if map.find_element(By.CLASS_NAME,'map-statistics-row-map-mapname').text in maps[i]: 
                map.click()
                time.sleep(1)
                stats = driver.find_element(By.CLASS_NAME,'map-statistics-extended.active')

                _5v4.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[0].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)
                _4v5.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[1].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)
                pistol.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[2].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)

                driver.find_element(By.CLASS_NAME,'map-statistics-row.active').click()
                found = True
        if found == False: 
            _5v4.append(0.0)
            _4v5.append(0.0)
            pistol.append(0.0)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])  # Switch to the first tab at the end of parsing first team
    time.sleep(5)

####
driver.find_element(By.CLASS_NAME,"analytics-center-button").click()
time.sleep(5)

#variables
rounds_lost = [] #here firstly stats for one team, then for another
rounds_won = [] #here firstly stats for one team, then for another
first_pick = [] #here one for one team, second for another, ....
first_pick_pc = [] #here one for one team, second for another, ....
rating_3m = [] #here firstly stats for one team, then for another
rating_event = [] #here firstly stats for one team, then for another
num_maps = []
winrate = [] #here one for one team, second for another, ....
maps_played = [] #here one for one team, second for another, ....

team_names.append(driver.find_element(By.CLASS_NAME,'head-to-head-section').find_elements(By.CLASS_NAME,'analytics-team-header')[0].find_element(By.CLASS_NAME,'team-name').text)
team_names.append(driver.find_element(By.CLASS_NAME,'head-to-head-section').find_elements(By.CLASS_NAME,'analytics-team-header')[1].find_element(By.CLASS_NAME,'team-name').text)

for item in driver.find_element(By.CLASS_NAME, 'analytics-head-to-head-wrapper').find_elements(By.TAG_NAME, 'tbody'):
    sum_3m = 0
    sum_event = 0
    for index in range(5):
        try:
            sum_3m += float(item.find_elements(By.CLASS_NAME,'table-3-months')[index].text)
        except:
            sum_3m += 0.86
        try:
            sum_event += float(item.find_elements(By.CLASS_NAME,'table-event')[index].text)
        except:
            try:
                sum_event += float(item.find_elements(By.CLASS_NAME,'table-3-months')[index].text)
            except:
                sum_event += 0.86
    
    rating_3m.append(sum_3m)
    rating_event.append(sum_event)

for item in driver.find_elements(By.CLASS_NAME,'match-map-count'):
    num_maps.append(float(item.text.split()[2]))



map_holder = driver.find_element(By.CLASS_NAME,'analytics-handicap-map-wrapper.g-grid')
for team_stats in map_holder.find_elements(By.CLASS_NAME,'col-6'):
    for map in team_stats.find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr'):
        lost = map.find_elements(By.CLASS_NAME,'analytics-handicap-map-data-avg')[0].text
        won = map.find_elements(By.CLASS_NAME,'analytics-handicap-map-data-avg')[1].text
        if lost != '-' and won != '-':
            rounds_lost.append(float(lost))
            rounds_won.append(float(won))
        elif lost != '-' and won == '-':
            rounds_lost.append(float(lost))
            rounds_won.append(0.0)
        elif lost == '-' and won != '-':
            rounds_lost.append(0.0)
            rounds_won.append(float(won))
        else:
            rounds_lost.append(0.0)
            rounds_won.append(0.0)

veto_stats = driver.find_element(By.CLASS_NAME,'analytics-map-stats').find_element(By.TAG_NAME,'tbody')
for row in veto_stats.find_elements(By.TAG_NAME,'tr'):
    try:
        first_pick_pc.append(float(row.find_element(By.CLASS_NAME,'analytics-map-stats-pick-percentage').text[:-1])/100)
    except:
        first_pick_pc.append(0.0)
    try:
        winrate.append(float(row.find_element(By.CLASS_NAME, "analytics-map-stats-win-percentage").text[:-1])/100)
    except:
        winrate.append(0.0)
    maps_played.append(float(row.find_element(By.CLASS_NAME, "analytics-map-stats-played").text))

    try:
        if row.find_element(By.CLASS_NAME,'analytics-map-stats-comment').find_element(By.CLASS_NAME,'comment.neutral').text == 'First pick':
            first_pick.append(True)
        else:
            first_pick.append(False)
    except:
        first_pick.append(False)

print("team_rating")
print(team_rating)
print("ranking")
print(ranking)
print("matches_winstreak")
print(matches_winstreak)
print("h2h")
print(h2h)
print("_5v4")
print(_5v4)
print("_4v5")
print(_4v5)
print("pistol")
print(pistol)
print("team_names")
print(team_names)
print('rating_3m')
print(rating_3m)
print('rating_event')
print(rating_event)
print('num_maps')
print(num_maps)
print('winrate')
print(winrate)
print('maps_played')
print(maps_played)
print('rounds_lost')
print(rounds_lost)
print('rounds_won')
print(rounds_won)
print('first_pick')
print(first_pick)
print('first_pick_pc')
print(first_pick_pc)
