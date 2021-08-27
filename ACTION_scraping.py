import selenium
from selenium import webdriver
import pandas as pd 
import matplotlib.pyplot as plt
from time import sleep
import requests
import numpy as np

from bs4 import BeautifulSoup as bs

# selenium broswer 
url = "https://www.imdb.com/list/ls009668579/"
#my_driver = "chromedriver.exe" 
driver = webdriver.Chrome("chromedriver.exe")
driver.get(url)
sleep(1)

#soup 
page = requests.get(url)

soup = bs(page.content , "html.parser")
url = "https://www.imdb.com/list/ls009668579/"

#list of names and the release dates
m_frame = soup.find("div" , class_ = "lister-list")
m_name = m_frame.findAll("h3", class_="lister-item-header")
m_name_list =[name.text.strip().split("\n") for name in m_name] 
m_name_list_t = np.array(m_name_list).T.tolist()
m_names = m_name_list_t[:][1]
m_r_date = m_name_list_t[:][2]
#m_r_dates stands for movie dates but it is little bit dirty  this is why im going to replace and strip and split
m_r_dates = [i.replace("("," ").replace(")","").replace("I","").strip() for i in m_r_date]

#movie description
m_desc = m_frame.findAll("p",class_ ="" )
m_desc_list = [d.text.strip().split("\n") for d in m_desc]

directors = []
stars = []
for i in range(1, 101):
    dirstars = driver.find_element_by_xpath( '//*[@id="main"]/div/div[3]/div[3]/div[' + str(i) + ']/div[2]/p[3]')
    dirs = dirstars.text.split('|')[0]
    dirs = dirs.split(sep=None, maxsplit=1)[1]
    directors.append(dirs)
    strs = dirstars.text.split('|')[1]
    strs = strs.split(sep=None, maxsplit=1)[1]
    stars.append(strs)

    
metascores = []
metascore = driver.find_elements_by_class_name('metascore')
for meta in metascore:
    metascores.append(meta.text)

#genre
m_genre = m_frame.findAll("span", class_ = "genre")
m_genre_list =[genre.text.strip().split("\n") for genre in m_genre]

#duration
m_duration = m_frame.findAll("span", class_ = "runtime")
m_duration_list = [dur.text.strip() for dur in m_duration]
duration_list = []
for dur in m_duration_list:
    m = dur.split()
    duration_list.append(m[0])

#box office gross
gross = []
for i in range (1, 101):
    try:
        bogross = driver.find_element_by_xpath( '//*[@id="main"]/div/div[3]/div[3]/div[' + str(i) + ']/div[2]/p[4]/span[5]')
        bogross = bogross.text.replace('$', '').replace('M','')
        gross.append(bogross.text)
    except:
        gross.append('Unavailable')

ratings =[]
for i in range (1, 101):
    rating = driver.find_element_by_xpath( '//*[@id="main"]/div/div[3]/div[3]/div[' + str(i) + ']/div[2]/div[1]/div[1]/span[2]')
    ratings.append(rating.text)

data = {
    'Movie':m_names,
    'Year of release': m_r_dates,
    'Genre': m_genre_list,
    'Directed by': directors,
    'Starring': stars,
    'Synopsis': m_desc_list,
    #'Box Office Gross in Million Dollars': gross,
    'Duration in minutes':duration_list,
    'IMDB User Rating': ratings,
    'Metascore from Metacritic': metascores
}   

df = pd.DataFrame(data)
