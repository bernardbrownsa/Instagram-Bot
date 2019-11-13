import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import smtplib
import time
import bb_info
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import re
import pickle
import Levenshtein as lev

followers = []
random_int = random.randint(0, 4)
#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
class InstagramBot():
    def __init__(self, email, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', options=self.browserProfile)
        self.email = email
        self.password = password
        #self.browser.set_window_size(700, 900)

#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')

        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
        pickle.dump(self.browser.get_cookies() , open("insta_cookies.pkl","wb"))
        print('cookies downloaded')
        time.sleep(2)
#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    def loadcookies(self):
        self.browser.get('https://www.instagram.com/')
        cookies = pickle.load(open("insta_cookies.pkl", "rb"))
        for cookie in cookies:
            self.browser.add_cookie(cookie)
        self.browser.get('https://www.instagram.com/')
#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    def followWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Follow'):
            time.sleep(2)
            followButton.click()
            time.sleep(random_int)
#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    def getUserFollowers(self, username, max):
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
    
        followersList.click()
        actionChain = webdriver.ActionChains(self.browser)
        time.sleep(2)
        while (numberOfFollowersInList < max):
            followersList.click()
            
            actionChain.key_down(Keys.DOWN).key_up(Keys.DOWN).perform()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            #print(numberOfFollowersInList)
            time.sleep(1)
        
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            #print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        return followers

#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    def closeBrowser(self):
        self.browser.close()
#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    def like_photo(self, hashtags):
        pic_hrefs = []
        time.sleep(3)

        for hashtag in hashtags:
            self.browser.get('https://www.instagram.com/explore/tags/' + hashtag + '/')
            for i in range(1, 3):

                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                hrefs_in_view = self.browser.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                print("The amount of pictures are: " + str(len(pic_hrefs)))

        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            print('There are ',unique_photos,' remaining.')

            comment_options1 = ['Hi! ','Hey! ','Ayy! ',':D ',':) ','Wow! ']
            comment_options2 = ['This is so ','This picture is so ', 'This post is so ', 'I love this, its so ','Love it, its so ','This is frickin ','This is flippin ']
            comment_options3 = ['great!','awesome!','amazing!','fantastic!','creative!','beautiful!','inspirational!','incredible!','lovely!']
            comment_options4 = [' :)',' :D',' <3', ' :o']

            comment_text = random.choice(comment_options1) + random.choice(comment_options2) + random.choice(comment_options3) + random.choice(comment_options4)

            self.browser.get(pic_href)
            time.sleep(2)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#-----Like Action ----------------------------------------------------------------------------------------------- 
            try:
                time.sleep(random.randint(6, 15))
                like_button = lambda: self.browser.find_element_by_xpath('//span[@aria-label="Like"]').click()
                like_button().click()
            except Exception as e:
                time.sleep(2)
                unique_photos -= 1
#-----Comment Action ----------------------------------------------------------------------------------------------- 
            if ((random.randint(1, 2)) == 1):
                try:
                    comment_button = lambda: self.browser.find_element_by_xpath("//span[@aria-label='Comment']")
                    comment_button().click()
                except NoSuchElementException:
                    print('click failed')

                try:
                    comment_box_elem = lambda: self.browser.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
                    comment_box_elem().send_keys('')
                    comment_box_elem().clear()
                    for letter in comment_text:
                        comment_box_elem().send_keys(letter)
                        time.sleep((random.randint(1, 7) / 30))
                    time.sleep((random.randint(1, 5)))
                    print(comment_text)
                    comment_box_elem().send_keys(Keys.ENTER)

                except:
                    print('send keys failed')
            else:
                print('Skipped commenting') 
#-----Follow Action ----------------------------------------------------------------------------------------------- 
            if ((random.randint(1, 5)) == 1):
                try:
                    follow_button = lambda: self.browser.find_element_by_xpath("//button[@class='oW_lN _0mzm- sqdOP yWX7d        ']")
                    follow_button().click()
                except NoSuchElementException:
                    print('click failed') 
            else:
                print('Skipped following')               
#--------------------------------------------------------------------------------------------------------------------------------

        for second in reversed(range(0, random.randint(18, 28))):
            print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                            + " | Sleeping " + str(second))
            time.sleep(1)

#IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    def closeBrowser(self):
        self.browser.close()
    
'''
----------------------------------------------------------------------------------
Actual code that is run 
----------------------------------------------------------------------------------
'''

# bot = InstagramBot('ItsJamieLizz', 'Gb51wam0')
bot = InstagramBot(bb_info.ig_un, bb_info.ig_pw)

hashtags = ['carribeancruise']
# -------------LIKE AND COMMENT BOT -------------------------
while True:
    try:
        bot = InstagramBot('rhinowallet', '')
        bot.signIn()
        #bot.loadcookies()
        print('These are the hashtags: ', hashtags)
        bot.like_photo(hashtags)
        bot.closeBrowser()
        print('closed')
        time.sleep((random.randint(250, 650)))
    except Exception:
        bot.closeBrowser()
        time.sleep(200)

