import requests
import pandas as pd
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os
import re


# set up the path to the chrome driver
chrome_path = os.getenv('CHROMEDRIVER_PATH', r'/Users/greg.anderson/personal_repos/chromedriver/chromedriver 3')

# set up the headless driver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")

# set the main url to scrape from
main_url = 'https://hashtagbasketball.com/fantasy-basketball-projections'
driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_path)

# get the html page as adriver object
driver.get(main_url)	
html = driver.page_source

# extract the html data from the website and parse it to a variable
soup = BeautifulSoup(html, 'lxml')

# choose all players
drop_down = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_DDSHOW"]/option[6]')
drop_down.click()

drop_down = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_DDRANK"]/option[1]')
drop_down.click()


# wait for the table to load after selecting all
'''
	TO DO
		1. Change it from sleep to wait for until the element loads
'''
time.sleep(10)

# convert the page to a html structure
html = driver.page_source

# extract the html data from the website and parse it to a variable
soup = BeautifulSoup(html, 'lxml')

# get the player stats
player_stats = soup.find('table', id = 'ContentPlaceHolder1_GridView1')
df = pd.read_html(str(player_stats))[0]

# close the driver
driver.quit()

# clean up the columns
df['FGA'] = df['FG%'].str.split(' ').str[1].str.replace('(','').str.replace(')','').str.split('/').str[1]
df['FGM'] = df['FG%'].str.split(' ').str[1].str.replace('(','').str.replace(')','').str.split('/').str[0]

df['FTA'] = df['FT%'].str.split(' ').str[1].str.replace('(','').str.replace(')','').str.split('/').str[1]
df['FTM'] = df['FT%'].str.split(' ').str[1].str.replace('(','').str.replace(')','').str.split('/').str[0]

df = df[ df['R#'] != "R#" ]

# save the file to a local store
df.to_csv('../data/player_projections.csv', index = False)

