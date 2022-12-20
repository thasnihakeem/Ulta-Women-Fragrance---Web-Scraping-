# Importing libraries
import re
import ast
import csv
import time
import random
import warnings
import requests
import numpy as np
import pandas as pd
from time import sleep
from getpass import getpass
from lxml import etree as et
from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode
from IPython.display import clear_output
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

warnings.filterwarnings('ignore')
driver = webdriver.Chrome(ChromeDriverManager().install())

def extract_content(url):
    driver.get(url)
    page_content = driver.page_source
    product_soup = BeautifulSoup(page_content, 'html.parser')
    dom = et.HTML(str(product_soup))
    return dom

def brand(dom):
    try:                                                                         #try to get the data
        brand=(dom.xpath('//*[@class="Link_Huge Link_Huge--compact"]/text()'))   #get the Brand name of the listing
        df['brand'].iloc[each_product] = brand                                   #To add data to a column
        df[['brand']] = df[['brand']].astype(str)                                #converting to string
        df['brand'] = df['brand'].str.replace('[','')                            #Removing unwanted characters
        df['brand'] = df['brand'].str.replace(']','')
        df['brand'] = df['brand'].str.replace("'",'')
    except:                                                                      #if the brand is not found, print the error message
        brand = "brand is not available"
        df['brand'].iloc[each_product] = brand   
    return  brand

def product(dom):
    try:                                                                                    #try to get the data
        product=(dom.xpath('//*[@class="Text-ds Text-ds--title-5 Text-ds--left"]/text()'))  #get the Product name of the listing
        df['product_name'].iloc[each_product] = product                                     #To add data to a column
        df[['product_name']] = df[['product_name']].astype(str)                             #converting to string
        df["product_name"] = df["product_name"].str.replace('[','')                         #Removing unwanted characters
        df["product_name"] = df["product_name"].str.replace(']','')
        df["product_name"] = df["product_name"].str.replace("'",'')
        df["product_name"] = df["product_name"].str.replace('"','')
    except:                                                                                 #if the product_name is not found, print the error message
        product = "product_name is not available"
        df['product'].iloc[each_product] = product   
    return  product

def reviews(dom):
    try:                                                                                                                 #try to get the data
        number_of_reviews=(dom.xpath('//*[@class="Text-ds Text-ds--body-3 Text-ds--left Text-ds--neutral-600"]/text()')) #get the number_of_reviews of the listing
        df['number_of_reviews'].iloc[each_product] = number_of_reviews                                                   #To add data to a column
        df[['number_of_reviews']] = df[['number_of_reviews']].astype(str)                                                #converting to string
        df["number_of_reviews"] = df["number_of_reviews"].str.replace(',','')                                            #Removing unwanted characters
        df["number_of_reviews"] = df["number_of_reviews"].str.replace('(','')
        df["number_of_reviews"] = df["number_of_reviews"].str.replace(')','')
        df["number_of_reviews"] = df["number_of_reviews"].str.replace('[','')
        df["number_of_reviews"] = df["number_of_reviews"].str.replace(']','')
        df["number_of_reviews"] = df["number_of_reviews"].str.replace("'size:'",'')
        df["number_of_reviews"] = df["number_of_reviews"].str.replace("'",'')
    except:                                                                                                             #if the number_of_reviews is not found, print the error message                                       
        number_of_reviews = "number_of_reviews is not available"
        df['number_of_reviews'].iloc[each_product] = number_of_reviews   
    return  number_of_reviews


def star_rating(dom):
    try:                                                                                       #try to get the data
        star_rating=(dom.xpath('//*[@class="Text-ds Text-ds--body-3 Text-ds--left"]/text()'))  #get the star_rating of the listing
        df['star_rating'].iloc[each_product] = star_rating                                     #To add data to a column
        df[['star_rating']] = df[['star_rating']].astype(str)                                  #converting to string
        df["star_rating"] = df["star_rating"].str.replace(']','')                              #Removing unwanted characters
        df["star_rating"] = df["star_rating"].str.replace('[','')
        df["star_rating"] = df["star_rating"].str.replace('Q & A','')
    except:                                                                                    #if the star_rating is not found, print the error message 
        star_rating = "star_rating is not available"
        df['star_rating'].iloc[each_product] = star_rating   
    return  star_rating

def Price():
    try:                                                                                                         #try to get the data
        Prices=driver.find_element(By.XPATH,'//*[@id="1b7a3ab3-2765-4ee2-8367-c8a0e7230fa4"]/span').text         #get the Price of the listing
    except:                                                                                                      #if the Price is not found, print the error message
        Prices = "Price is not available" 
    return Prices

def ingredients(dom):
    try:                                                                                                                   #try to get the data
        Ingredients=(dom.xpath('//*[@id="bb5f7945-7101-402b-b8b3-1ad025315d50"]/div/div/details[3]/div/div/p[1]/text()'))  #get the Ingredients of the listing
        df['Ingredients'].iloc[each_product] = Ingredients                                                                 #To add data to a column 
        df[['Ingredients']] = df[['Ingredients']].astype(str)                                                              #converting to string
        df["Ingredients"] = df["Ingredients"].str.replace('[','')                                                          #Removing unwanted characters
        df["Ingredients"] = df["Ingredients"].str.replace(']','')
    except:                                                                                                                #if the Ingredients is not found, print the error message 
        Ingredients = "Ingredients is not available"
        df['Ingredients'].iloc[each_product] = Ingredients   
    return  Ingredients
    
def Fragrance_Description():
    try:                                                                                                                #try to get the data
        Fragrance_Descriptions=driver.find_element(By.XPATH,'//*[@id="b46bc3ad-9907-43a6-9a95-88c160f02d7f"]/p').text   #get the Fragrance_Description of the listing
    except:                                                                                                             #if the Fragrance_Description is not found, print the error message 
        Fragrance_Descriptions = "Fragrance_Description is not available" 
    return Fragrance_Descriptions

def Detail():
    try:                                                                   #try to get '+' button
        driver.find_element(By.XPATH,'//*[@id="Details"]').click()         #to click the '+' button of the in the site to get the details data
    except:                                                                #to pass it ,if '+' button can't be located
        pass
    time.sleep(3)
    try:                                                                                                                   #try to get the data
        Details = driver.find_element(By.XPATH,'//*[@id="bb5f7945-7101-402b-b8b3-1ad025315d50"]/div/div/details[1]').text  #get the Details of the listing                                                                        #To add data to a column
    except:                                                                                                                #if the Details is not found, print the error message
        Details = "Details is not available"
    return Details                                                                                 


# Ulta website link
URL="https://www.ulta.com/womens-fragrance?N=26wn"

#list to store the url of every resultant page
base_url_link = [URL]   #list of base url
while URL!=[]:                                                            
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    for all_pages in soup.find_all('li', class_="next-prev floatl-span"):   #get the all resultant page url of the listing
        x=all_pages.find('a',class_='next')
        if x:
            a="https://www.ulta.com" + x['href']                            #converting to valid url
            base_url_link.append("https://www.ulta.com" + x['href'])        #storing all rasultant page link in a list   
            URL=a

        else:
            URL=[] 
base_url_links=set(base_url_link)       # converting base_url_link to set to get unique values        
page_lst_link=list(base_url_links)      # converting to list

# Fetching all resulted product links
product_links = []
for i in  page_lst_link: 
    response = requests.get(i)
    soup = BeautifulSoup(response.content, 'html.parser')
    for row in soup.find_all('p', class_='prod-desc'):                #get the all resultant product url of the listing
        main_box=(row.a['href'])
    for row in soup.find_all('p', class_='prod-desc'):
        product_links.append("https://www.ulta.com" + row.a['href'])  #converting to valid url  and storing it in a list

# Indicate scraping completion
print(f'Got All Brand Links! There are {len(product_links)} brands in total.')

# Creating a dictionary of the required columns
data_dic = {'product_url': [], 'brand': [], 'product_name': [],'number_of_reviews': [], 'Details': [], 'star_rating': [],'price':[], 'Fragrance Description':[],'Ingredients':[]}

# Creating a dataframe with those columns
df=pd.DataFrame(data_dic)

# Assigning the scraped links to the column 'product_url'
df['product_url']=product_links

# Scraping data like 'brand_name','product_name','number_of_reviews','love_count','star_rating'  and 'ingredients'
for each_product in range(len(df)):
    product_url = df['product_url'].iloc[each_product]
    product_content = extract_content(product_url)
    brand(product_content)                                 # brands
    product(product_content)                               # product_name
    reviews(product_content)                               # number_of_review
    star_rating(product_content)                           # star_rating
    ingredients(product_content)                           #ingredients
    
# Scraping 'price' ,'Fragrance Description' dataand 'Details' data
for each_product in range(len(df)):
    driver.get(df['Product_url'].iloc[each_product])               
    price=Price()                                                                   #Price
    df["Price"].iloc[each_product]= price                                           #To add data to a column
    df[["Price"]] = df[['Price']].astype(str)                                       #converting to string
    df["Price"] = df["Price"].str.replace('[','')                                   #Removing unwanted characters
    df["Price"] = df["Price"].str.replace(']','')
    df["Price"] = df["Price"].str.replace('$','')
    df["Price"] = df["Price"].str.replace("'",'')
    
    fragrance_description=Fragrance_Description()                                   #Fragrance Description
    df['Fragrance Description'].iloc[each_product] = fragrance_description          #To add data to a column
    df[['Fragrance Description']] = df[['Fragrance Description']].astype(str)       #converting to string 
    df["Fragrance Description"] = df["Fragrance Description"].str.replace('[','')   #Removing unwanted characters                                                          #Removing unwanted characters
    df["Fragrance Description"] = df["Fragrance Description"].str.replace(']','')

    details=Detail()                                                                #Details
    df['Details'].iloc[each_product] = details                                      #To add data to a column

    pz=None
    dt=None     
    
# to print data
print(df) 

# Convering data to a csv file
df.to_csv("Ulta_Women_Fragrance_Data")
