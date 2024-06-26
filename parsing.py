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

class Parser:
    
    def start_driver(self):
        self.driver = uc.Chrome()

    def parse_event(self, url, event):
        self.driver.get(url)
        time.sleep(10)

        #variables for dataset        
        #should be updated each iteration
        team_names = []
        maps = []
        y_true = []

        num_maps = []
        winstreak = []
        h2h = []
        ranking = []
        weeks = []
        age = []
        map_winrate = []
        maps_played = []
        _5v4 = []
        _4v5 = []
        pistol = []
        rating_3m = []

        #temporary variables
        temp_teams = []
        temp_maps = []

        search = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "navsearchinput.tt-input.js-bound"))
        )
        search.click()

        search.send_keys(event)
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME,'fa.fa-search').click()
        time.sleep(3)
        self.driver.find_element(By.CLASS_NAME,'table').find_element(By.TAG_NAME,'a').click()

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME,'event-hub-link'))
        )
        self.driver.find_elements(By.CLASS_NAME,'event-hub-link')[1].click()

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME,'result'))
        )
        num = len(self.driver.find_elements(By.CLASS_NAME,'result'))
        #winstreaks
        for match_order in range(num):
            #need to go to results page?
            matches = self.driver.find_elements(By.CLASS_NAME,'result')

            action_chains = ActionChains(self.driver)
            action_chains.key_down(Keys.CONTROL).click(matches[match_order]).key_up(Keys.CONTROL).perform()
            time.sleep(5)
            self.driver.switch_to.window(self.driver.window_handles[-1])  # Switch to the second tab/window (index 1)

            temp_teams.append(self.driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[0].text)
            temp_teams.append(self.driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[1].text)

            team_names.append(self.driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[0].text)
            team_names.append(self.driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[1].text)


            past_matches = self.driver.find_elements(By.CLASS_NAME,'past-matches-box.text-ellipsis')[2:]   
            for box in past_matches[:2]:
                try:
                    streak = box.find_element(By.CLASS_NAME,'past-matches-streak')
                except:
                    winstreak.append(0.0)
                    continue
                else:
                    winstreak.append(float(streak.text[0]))

            #H2h
            h2h.append(float(self.driver.find_element(By.CLASS_NAME,'flexbox-column.flexbox-center.grow.right-border').find_element(By.CLASS_NAME,'bold').text))
            h2h.append(float(self.driver.find_element(By.CLASS_NAME,'flexbox-column.flexbox-center.grow.left-border').find_element(By.CLASS_NAME,'bold').text))

            for map in self.driver.find_elements(By.CLASS_NAME,'mapholder'):
                    try:
                        temp_maps.append(map.find_element(By.CLASS_NAME,'played').find_element(By.TAG_NAME,'img').get_attribute('title'))
                        maps.append(map.find_element(By.CLASS_NAME,'played').find_element(By.TAG_NAME,'img').get_attribute('title'))
                        y_true.append(float(temp_teams.index(map.find_element(By.CLASS_NAME,'results.played').find_element(By.CLASS_NAME,'won').find_element(By.TAG_NAME,'img').get_attribute('title'))))
                    except:
                        continue
            
            num_maps.append(len(temp_maps))

            for team in range(2):
                action_chains = ActionChains(self.driver)
                action_chains.key_down(Keys.CONTROL).click(self.driver.find_elements(By.CLASS_NAME,'team')[team]).key_up(Keys.CONTROL).perform()
                time.sleep(5)
                self.driver.switch_to.window(self.driver.window_handles[-1])  # Switch to the second tab/window (index 1)

                stats = self.driver.find_elements(By.CLASS_NAME,'profile-team-stat')

                ranking.append(float(stats[0].find_element(By.CLASS_NAME,'right').text[1:]))
                weeks.append(float(stats[1].find_element(By.CLASS_NAME,'right').text))
                try:
                    age.append(float(stats[2].find_element(By.CLASS_NAME,'right').text))
                except:
                    age.append(23.0)

                self.driver.find_elements(By.CLASS_NAME,'tab.text-ellipsis')[-1].click()
                #need rework?
                for cur in temp_maps:
                    for map in self.driver.find_elements(By.CLASS_NAME,'map-statistics-row'):
                        if map.find_element(By.CLASS_NAME,'map-statistics-row-map-mapname').text in cur:
                            map_winrate.append(float(map.find_element(By.CLASS_NAME,'map-statistics-row-win-percentage').text[:-1])/100)
                            map.click()

                            time.sleep(1)
                            stats = self.driver.find_element(By.CLASS_NAME,'map-statistics-extended.active')

                            maps_played.append(float(stats.find_elements(By.CLASS_NAME,'stat')[0].text) + float(stats.find_elements(By.CLASS_NAME,'stat')[2].text))
                            _5v4.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[0].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)
                            _4v5.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[1].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)
                            pistol.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[2].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)

                            self.driver.find_element(By.CLASS_NAME,'map-statistics-row.active').click()

                self.driver.find_elements(By.CLASS_NAME,'moreButton')[-1].click()
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME,'stats-top-menu-item.stats-top-menu-item-link'))
                )

                self.driver.find_elements(By.CLASS_NAME,'stats-top-menu-item.stats-top-menu-item-link')[3].click()
                Select(self.driver.find_element(By.CLASS_NAME,'stats-sub-navigation-simple-filter-time')).select_by_index(2)
                time.sleep(2)
                sum=0
                for stat in self.driver.find_element(By.CLASS_NAME,'stats-table.player-ratings-table').find_elements(By.CLASS_NAME,'ratingCol')[1:]:
                    sum += float(stat.text)
                rating_3m.append(sum)

                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[1])  # Switch to the first tab at the end of parsing first team

                time.sleep(5)

            print("team_names")
            print(team_names)
            print("y_true")
            print(y_true)
            print("maps")
            print(maps)
            print("temp_maps")
            print(temp_maps)
            print("num_maps")
            print(num_maps)
            print("winstreak")
            print(winstreak)
            print("h2h")
            print(h2h)
            print("ranking")
            print(ranking)
            print("weeks")
            print(weeks)
            print("age")
            print(age)
            print("map_winrate")
            print(map_winrate)
            print("maps_played")
            print(maps_played)
            print("_5v4")
            print(_5v4)
            print("_4v5")
            print(_4v5)
            print("pistol")
            print(pistol)
            print("rating_3m")
            print(rating_3m)

            temp_maps.clear()
            temp_teams.clear()
            
            self.driver.close()    
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)


        self.driver.quit()
        return team_names,y_true,maps,num_maps,winstreak,h2h,ranking,weeks,age,map_winrate,maps_played,_5v4,_4v5,pistol,rating_3m

    def parse_event_rating(self, url, event):
        self.driver.get(url)
        time.sleep(10)

        #variables for dataset
        teams = []
        team_rating = []
        event_rating = []

        search = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "navsearchinput.tt-input.js-bound"))
        )
        search.click()

        search.send_keys(event)
        time.sleep(2)
        self.driver.find_element(By.CLASS_NAME,'fa.fa-search').click()
        time.sleep(3)
        self.driver.find_element(By.CLASS_NAME,'table').find_element(By.TAG_NAME,'a').click()

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME,'event-hub-link'))
        )
        self.driver.find_elements(By.CLASS_NAME,'event-hub-link')[3].click()

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME,'stats-section.stats-team.stats-sidebar'))
        )
        self.driver.find_elements(By.CLASS_NAME,'sidebar-single-line-item')[2].click()

        table = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME,'stats-table.player-ratings-table'))
        )
        rows = table.find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr')
        num_teams = len(rows)
        for index in range(num_teams):
            names = self.driver.find_element(By.CLASS_NAME,'stats-table.player-ratings-table').find_element(By.TAG_NAME,'tbody').find_elements(By.CLASS_NAME,'teamCol-teams-overview')
            ratings = self.driver.find_element(By.CLASS_NAME,'stats-table.player-ratings-table').find_element(By.TAG_NAME,'tbody').find_elements(By.CLASS_NAME,'ratingCol')
            
            teams.append(names[index].text)
            team_rating.append(float(ratings[index].text))

            action_chains = ActionChains(self.driver)
            action_chains.key_down(Keys.CONTROL).click(names[index].find_element(By.TAG_NAME,'a')).key_up(Keys.CONTROL).perform()
            time.sleep(5)
            self.driver.switch_to.window(self.driver.window_handles[-1])  # Switch to the second tab/window (index 1)

            self.driver.find_elements(By.CLASS_NAME,'stats-top-menu-item.stats-top-menu-item-link')[3].click()
            rats = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME,'stats-table.player-ratings-table'))
            )
            sum=0
            for stat in rats.find_elements(By.CLASS_NAME,'ratingCol')[1:]:
                sum += float(stat.text)
            event_rating.append(sum)

            print(teams)
            print(team_rating)
            print(event_rating)

            self.driver.close()    
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)
        
        self.driver.quit()
        return teams, team_rating, event_rating

    def parse_bet(self, url):
        self.driver.get(url)
        time.sleep(10)

        #variables
        team_names = []
        maps = ['Mirage','Inferno','Nuke','Overpass','Vertigo','Ancient','Anubis']
        rounds_lost = [] #here firstly stats for one team, then for another
        rounds_won = [] #here firstly stats for one team, then for another
        first_pick = [] #here one for one team, second for another, ....
        first_pick_pc = [] #here one for one team, second for another, ....

        team_names.append(self.driver.find_element(By.CLASS_NAME,'head-to-head-section').find_elements(By.CLASS_NAME,'analytics-team-header')[0].find_element(By.CLASS_NAME,'team-name').text)
        team_names.append(self.driver.find_element(By.CLASS_NAME,'head-to-head-section').find_elements(By.CLASS_NAME,'analytics-team-header')[1].find_element(By.CLASS_NAME,'team-name').text)

        map_holder = self.driver.find_element(By.CLASS_NAME,'analytics-handicap-map-wrapper.g-grid')
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

        veto_stats = self.driver.find_element(By.CLASS_NAME,'analytics-map-stats').find_element(By.TAG_NAME,'tbody')
        for row in veto_stats.find_elements(By.TAG_NAME,'tr'):
            try:
                first_pick_pc.append(float(row.find_element(By.CLASS_NAME,'analytics-map-stats-pick-percentage').text[:-1])/100)
            except:
                first_pick_pc.append(0.0)

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

        self.driver.quit()
        return team_names, rounds_lost, rounds_won, first_pick, first_pick_pc

    def inference(self, match):
        self.driver.get(match)
        time.sleep(10)

        team_names = []
        team_rating = [0.95,0.95]
        team_names.append(self.driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[0].text)
        team_names.append(self.driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_elements(By.CLASS_NAME,'teamName')[1].text)
        action_chains = ActionChains(self.driver)
        action_chains.key_down(Keys.CONTROL).click(self.driver.find_element(By.CLASS_NAME,'standard-box.teamsBox').find_element(By.CLASS_NAME,'event.text-ellipsis')).key_up(Keys.CONTROL).perform()
        time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        try:
            self.driver.find_elements(By.CLASS_NAME,'event-hub-link')[3].click()
        except:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(5)
        else:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME,'stats-section.stats-team.stats-sidebar'))
            )
            self.driver.find_elements(By.CLASS_NAME,'sidebar-single-line-item')[2].click()
            try:
                for item in self.driver.find_element(By.CLASS_NAME,'stats-table.player-ratings-table').find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr'):
                    if item.find_element(By.TAG_NAME,'td').text in team_names:
                        team_rating[team_names.index(item.find_element(By.TAG_NAME,'td').text)] = float(item.find_element(By.CLASS_NAME,'ratingCol').text)
            except:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])  # Switch to the first tab at the end of parsing first team
                time.sleep(5)
            else:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                time.sleep(5)

        ranking = []
        matches_winstreak = []
        h2h = []

        try:
            ranking.append(float(self.driver.find_elements(By.CLASS_NAME,"teamRanking")[0].text.split("#")[1]))  
        except:
            ranking.append(250.0)

        try:
            ranking.append(float(self.driver.find_elements(By.CLASS_NAME,"teamRanking")[1].text.split("#")[1]))  
        except:
            ranking.append(250.0)

        h2h.append(float(self.driver.find_element(By.CLASS_NAME,'flexbox-column.flexbox-center.grow.right-border').find_element(By.CLASS_NAME,'bold').text))
        h2h.append(float(self.driver.find_element(By.CLASS_NAME,'flexbox-column.flexbox-center.grow.left-border').find_element(By.CLASS_NAME,'bold').text))

        past_matches = self.driver.find_elements(By.CLASS_NAME,'past-matches-box.text-ellipsis')[2:]   
        for box in past_matches[:2]:
            try:
                streak = box.find_element(By.CLASS_NAME,'past-matches-streak')
            except:
                matches_winstreak.append(0.0)
                continue
            else:
                matches_winstreak.append(float(streak.text[0]))
        #####
        maps = ['Mirage','Inferno','Nuke','Overpass','Vertigo','Ancient','Anubis']
        weeks = []
        age = []
        _5v4 = []
        _4v5 = []
        pistol = []
        for team in range(2):
            action_chains = ActionChains(self.driver)
            action_chains.key_down(Keys.CONTROL).click(self.driver.find_elements(By.CLASS_NAME,'team')[team]).key_up(Keys.CONTROL).perform()
            time.sleep(5)
            self.driver.switch_to.window(self.driver.window_handles[-1])  # Switch to the second tab/window (index 1)


            stats = self.driver.find_elements(By.CLASS_NAME,'profile-team-stat')
            weeks.append(float(stats[1].find_element(By.CLASS_NAME,'right').text))
            try:
                age.append(float(stats[2].find_element(By.CLASS_NAME,'right').text))
            except:
                age.append(23.0)


            self.driver.find_elements(By.CLASS_NAME,'tab.text-ellipsis')[-1].click()

            for i in range(len(maps)):
                found = False
                for map in self.driver.find_elements(By.CLASS_NAME,'map-statistics-row'):
                    if map.find_element(By.CLASS_NAME,'map-statistics-row-map-mapname').text in maps[i]: 
                        map.click()
                        time.sleep(1)
                        stats = self.driver.find_element(By.CLASS_NAME,'map-statistics-extended.active')

                        _5v4.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[0].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)
                        _4v5.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[1].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)
                        pistol.append(float(stats.find_elements(By.CLASS_NAME,'map-statistics-extended-general-stat')[2].find_elements(By.TAG_NAME,'div')[1].text[:-1])/100)

                        self.driver.find_element(By.CLASS_NAME,'map-statistics-row.active').click()
                        found = True
                if found == False: 
                    _5v4.append(0.0)
                    _4v5.append(0.0)
                    pistol.append(0.0)

            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])  # Switch to the first tab at the end of parsing first team
            time.sleep(5)

        ####
        self.driver.find_element(By.CLASS_NAME,"analytics-center-button").click()
        time.sleep(5)

        #variables
        rounds_lost = [] #here firstly stats for one team, then for another
        rounds_won = [] #here firstly stats for one team, then for another
        first_pick = [] #here one for one team, second for another, ....
        first_pick_pc = [] #here one for one team, second for another, ....
        rating_3m = [] #here firstly stats for one team, then for another
        rating_event = [] #here firstly stats for one team, then for another
        winrate = [] #here one for one team, second for another, ....
        maps_played = [] #here one for one team, second for another, ....

        for item in self.driver.find_element(By.CLASS_NAME, 'analytics-head-to-head-wrapper').find_elements(By.TAG_NAME, 'tbody'):
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

        map_holder = self.driver.find_element(By.CLASS_NAME,'analytics-handicap-map-wrapper.g-grid')
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

        veto_stats = self.driver.find_element(By.CLASS_NAME,'analytics-map-stats').find_element(By.TAG_NAME,'tbody')
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
        print("weeks")
        print(weeks)
        print("age")
        print(age)
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

        return team_names, team_rating, ranking, matches_winstreak, h2h, weeks, age, _4v5, _5v4, pistol, rounds_lost, rounds_won, first_pick, first_pick_pc, rating_3m, rating_event, winrate, maps_played


    def close_page(self):
        if hasattr(self, 'driver'):
            self.driver.close()

    def stop_driver(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
            del self.driver


if __name__ == "__main__":
    parser = Parser()
    parser.start_driver()

    parser.inference("https://www.hltv.org/matches/2367187/aurora-vs-apeks-esl-challenger-jnkping-2023-europe-closed-qualifier")