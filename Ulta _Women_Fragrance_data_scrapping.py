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
from urllib.request import urlopen as ureq
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

warnings.filterwarnings('ignore')
driver = webdriver.Chrome(ChromeDriverManager().install())

def extract_content(url):
    page_content = requests.get(url)
    product_soup = BeautifulSoup(page_content.content, 'html.parser')
    dom = et.HTML(str(product_soup))
    return dom

def brand(dom):
    brand=(dom.xpath('//*[@class="Link_Huge Link_Huge--compact"]/text()'))   #get the Brand name of the listing
    df['brand'].iloc[each_product] = brand                                   #To add data to a column
    df[['brand']] = df[['brand']].astype(str)                                #converting to string
    df['brand'] = df['brand'].str.replace('[','')                            #Removing unwanted characters
    df['brand'] = df['brand'].str.replace(']','')

def product(dom):
    product=(dom.xpath('//*[@class="Text-ds Text-ds--title-5 Text-ds--left"]/text()'))  #get the Product name of the listing
    df['product_name'].iloc[each_product] = product                                     #To add data to a column
    df[['product_name']] = df[['product_name']].astype(str)                             #converting to string
    df["product_name"] = df["product_name"].str.replace('[','')                         #Removing unwanted characters
    df["product_name"] = df["product_name"].str.replace(']','')

def reviews(dom):
    number_of_reviews=(dom.xpath('//*[@class="Text-ds Text-ds--body-3 Text-ds--left Text-ds--neutral-600"]/text()')) #get the number_of_reviews of the listing
    df['number_of_reviews'].iloc[each_product] = number_of_reviews                                                   #To add data to a column
    df[['number_of_reviews']] = df[['number_of_reviews']].astype(str)                                                #converting to string
    df["number_of_reviews"] = df["number_of_reviews"].str.replace(',','')                                            #Removing unwanted characters
    df["number_of_reviews"] = df["number_of_reviews"].str.replace('(','')
    df["number_of_reviews"] = df["number_of_reviews"].str.replace(')','')
    df["number_of_reviews"] = df["number_of_reviews"].str.replace('[','')
    df["number_of_reviews"] = df["number_of_reviews"].str.replace(']','')
    df["number_of_reviews"] = df["number_of_reviews"].str.replace('size:','')

def star_rating(dom):
    star_rating=(dom.xpath('//*[@class="Text-ds Text-ds--body-3 Text-ds--left"]/text()'))  #get the star_rating of the listing
    df['star_rating'].iloc[each_product] = star_rating                                     #To add data to a column
    df[['star_rating']] = df[['star_rating']].astype(str)                                  #converting to string
    df["star_rating"] = df["star_rating"].str.replace(']','')                              #Removing unwanted characters
    df["star_rating"] = df["star_rating"].str.replace('[','')
    df["star_rating"] = df["star_rating"].str.replace('Q & A','')

def price(driver):
    price=driver.find_element("xpath",'//*[@class="Text-ds Text-ds--title-6 Text-ds--left Text-ds--black"]').text()  #get the Price of the listing
    df['price'].iloc[each_product] = price                                                                           #To add data to a column
    df[['price']] = df[['price']].astype(str)                                                                        #converting to string
    df["Price"] = df["Price"].str.replace('[','')                                                                    #Removing unwanted characters
    df["Price"] = df["Price"].str.replace(']','')
    df["Price"] = df["Price"].str.replace('$','')
    df["Price"] = df["Price"].str.replace("'",'')
    
def ingredients(dom):
    Ingredients=(dom.xpath('//*[@id="bb5f7945-7101-402b-b8b3-1ad025315d50"]/div/div/details[3]/div/div/p[1]/text()'))  #get the Ingredients of the listing
    df['Ingredients'].iloc[each_product] = Ingredients                                                                 #To add data to a column 
    df[['Ingredients']] = df[['Ingredients']].astype(str)                                                              #converting to string
    df["Ingredients"] = df["Ingredients"].str.replace('[','')                                                          #Removing unwanted characters
    df["Ingredients"] = df["Ingredients"].str.replace(']','')
    
def Fragrance_Description(dom):
    Fragrance_Description=(dom.xpath('//*[@class="Text-ds Text-ds--subtitle-1 Text-ds--left"]/text()'))  #get the Fragrance_Description of the listing
    df['Fragrance Description'].iloc[each_product]=Fragrance_Description                                 #To add data to a column
    
def Details(driver):
    Details =driver.find_element_by_xpath('//*[@id="bb5f7945-7101-402b-b8b3-1ad025315d50"]/div/div/details[1]').text()  #get the Details of the listing
    df['Details'].iloc[each_product] = Details                                                                          #To add data to a column


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
data_dic = {'product_url': [], 'brand': [], 'product_name': [],'number_of_reviews': [], 'Details': [], 'star_rating': [],'price':[], 'Fragrance Family':[],'Scent Type':[],'Key Notes':[],'Features':[],'Fragrance Description':[],'Composition':[],'Ingredients':[]}

# Creating a dataframe with those columns
df=pd.DataFrame(data_dic)

# Assigning the scraped links to the column 'product_url'
df['product_url']=product_links

# Scraping data like 'brand_name','product_name','number_of_reviews','love_count','star_rating'  and 'ingredients'
for each_product in range(len(df)):
    product_url = df['product_url'].iloc[each_product]
    product_content = extract_content(product_url)

    try: #try to get the data
         # brands
        brand(product_content)

         # product_name
        product(product_content)

         # number_of_reviews
        reviews(product_content)

         # star_rating
        star_rating(product_content)
        
         #ingredients
        ingredients(product_content)

         #Fragrance Description
        Fragrance_Description(product_content)
        
    except: #if the Data is not found, to get raw empty
        pass
    

# Scraping 'price' data
for each_product in range(len(data)):
    driver.get(df['product_url'].iloc[each_product])
    
    try:                                 #try to get the price data
        price(product_content)
    except:                              #if the data is not found,to get the raw empty
        pass  
    
    
# Scraping the remaining data like 'Fragrance Family','Scent Type','Key Notes' and 'Composition','Features'
for each_product in range(len(data)):
    driver.get(data['product_url'].iloc[each_product])
    
# Scraping the 'Details' data
    try:                                                             #try to get '+' button
        driver.find_element_by_xpath('//*[@id="Details"]').click()   #to click the '+' button of the in the site to get the details data
    except:                                                          #to pass it ,if '+' button can't be located
        pass
    time.sleep(3)
    try:                                           #try to get the details data
        Details(product_content)
    except:                                        #if it is not found ,to get the raw empty
        pass

#converting 'Details' TO A dictionary
df['Details']=df['Details'].apply(lambda x:x.strip('][').split(', ')) #to strip and split the 'Details' data
for i in range(len(df)):
    dic={}                                                            #Creating a empty dictionary to store the key-value data
    while dic=={}:
        keys=[]                                                       #creating empty list to store keys
        values=[]                                                     #creating empty list to store keys
        for p in range(len(df['Details'].iloc[i])): 
            section=df['Details'].iloc[i][p]
            section=section.strip("''")                               #strping the 'Details' data
            split_section = section.split('\\n')                      #splitting the 'Details' data
        #     print(split_section)
            
            for j in range(len(split_section)):
                if split_section[j]=='Composition':                  #to get 'Composition' from 'Details' data
                    keys.append(split_section[j])                    #append the key to the key list
                    values.append(split_section[j+1])                #append the value to the value list


                if split_section[j]=='Fragrance Family':             #to get 'Fragrance Family' from 'Details' data
                    keys.append(split_section[j])                    #append the key to the key list
                    values.append(split_section[j+1])                #append the value to the value list


                if split_section[j]=='Key Notes':                    #to get 'Key Notes' from 'Details' data
                    keys.append(split_section[j])                    #append the key to the key list
                    values.append(split_section[j+1])                #append the value to the value list

                if split_section[j]=='Features':                     #to get 'Features' from 'Details' data
                    keys.append(split_section[j])                    #append the key to the key list
                    values.append(split_section[j+1])                #append the value to the value list


                if split_section[j]=='Scent Type':                   #to get 'Scent Type' from 'Details' data
                    keys.append(split_section[j])                    #append the key to the key list
                    values.append(split_section[j+1])                #append the value to the value list
                    
        
                if (p==len(df['Details'].iloc[i])-1) and (j==len(split_section)-1) and (keys==[]):
                    dic=np.nan                                       #if the data note found ,to print NaN value
     
            try:                                                     #try to get the data

                for l in range(len(keys)):
                    dic[keys[l]]=values[l]                           #to store the keys and values in empty dictionary
            except:
                pass                                                 #if the data note found ,to let it pass
            
    df['Details'][i]=dic                                             #to add the dictionary to 'Details' column
    
    
# extracting 'Fragrance Family','Scent Type','Key Notes' and 'Composition' data from 'Details' Dictionary
for i in range(len(df)):                                       #to store the keys and values in empty dictionary
    try:
        df['Details'][i]=ast.literal_eval(df['Details'][i])    #safely evaluate strings containing data from unknown sources
    except:                                                    #if the data note found ,to let it pass
        pass
    
df=df[df['Details'].apply(lambda x: isinstance(x, dict))]      #converting object to dictionary

for i in range(len(df)):
    df['Fragrance Family'].iloc[i]=df['Details'].iloc[i].get('Fragrance_Family') #To add 'Fragrance Family' data to 'Fragrance Family' column

for i in range(len(df)):
    df['Scent_Type'].iloc[i]=df['Details'].iloc[i].get('Scent_Type')             #To add 'Scent_Type' data to 'Scent_Type' column

for i in range(len(df)):
    df['Key_Notes'].iloc[i]=df['Details'].iloc[i].get('Key_Notes')               #To add 'Key_Notes' data to 'Key_Notes' column   
    
for i in range(len(df)):
    df['Features'].iloc[i]=df['Details'].iloc[i].get('Features')                 #To add 'Features' data to 'Features' column

for i in range(len(df)):
    df['Composition'].iloc[i]=df['Details'].iloc[i].get('Composition')           #To add 'Composition' data to 'Composition' column
    
# to print data
print(df) 

# Convering data to a csv file
df.to_csv("Ulta_Women_Fragrance_Data")
