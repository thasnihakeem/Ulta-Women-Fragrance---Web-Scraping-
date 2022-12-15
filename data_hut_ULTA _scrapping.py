# Importing libraries
import re
import ast
import csv
import time
import random
import warnings
import requests
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
    brand=(dom.xpath('//*[@class="Link_Huge Link_Huge--compact"]/text()'))
    df['brand'].iloc[each_product] = brand

def product(dom):
    product=(dom.xpath('//*[@class="Text-ds Text-ds--title-5 Text-ds--left"]/text()'))
    df['product_name'].iloc[each_product] = product

def reviews(dom):
    number_of_reviews=(dom.xpath('//*[@class="Text-ds Text-ds--body-3 Text-ds--left Text-ds--neutral-600"]/text()'))
    df['number_of_reviews'].iloc[each_product] = number_of_reviews

def star_rating(dom):
    star_rating=(dom.xpath('//*[@class="Text-ds Text-ds--body-3 Text-ds--left"]/text()'))
    df['star_rating'].iloc[each_product] = star

def price(driver):
    price=driver.find_element("xpath",'//*[@class="Text-ds Text-ds--title-6 Text-ds--left Text-ds--black"]').text()
    df['price'].iloc[each_product] = price
    
def ingredients(dom):
    Ingredients=(dom.xpath('//*[@id="bb5f7945-7101-402b-b8b3-1ad025315d50"]/div/div/details[3]/div/div/p[1]/text()'))
    df['Ingredients'].iloc[each_product] = Ingredients  
    
def Fragrance_Description(dom):
    Fragrance_Description=(dom.xpath('//*[@class="Text-ds Text-ds--subtitle-1 Text-ds--left"]/text()'))
    df['Fragrance Description'].iloc[each_product]=Fragrance_Description
    
def Details(driver):
    Details =driver.find_element_by_xpath('//*[@id="bb5f7945-7101-402b-b8b3-1ad025315d50"]/div/div/details[1]').text()
    df['Details'].iloc[each_product] = Details


# Ulta website link
URL="https://www.ulta.com/womens-fragrance?N=26wn"
link = [URL]

while URL!=[]:
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    for all_pages in soup.find_all('li', class_="next-prev floatl-span"):
        x=all_pages.find('a',class_='next')
        if x:
            a="https://www.ulta.com" + x['href']
            link.append("https://www.ulta.com" + x['href'])
            URL=a

        else:
            URL=[] 
links=set(link)           
page_lst_link=list(links)

# Fetching all resulted product links
product_links = []
for i in  page_lst_link: 
    response = requests.get(i)
    soup = BeautifulSoup(response.content, 'html.parser')
    for row in soup.find_all('p', class_='prod-desc'):
        main_box=(row.a['href'])
    for row in soup.find_all('p', class_='prod-desc'):
        product_links.append("https://www.ulta.com" + row.a['href'])

# Indicate scraping completion
print(f'Got All Brand Links! There are {len(product_links)} brands in total.')

# Creating a dictionary of the required columns
data_dic = {'product_url': [], 'brand': [], 'product_name': [],'number_of_reviews': [], 'Details': [], 'star_rating': [],'price':[], 'Fragrance Family':[],'Scent Type':[],'Key Notes':[],'Features':[],'Fragrance Description':[],'COMPOSITION':[],'Ingredients':[]}

# Creating a dataframe with those columns
df=pd.DataFrame(data_dic)

# Assigning the scraped links to the column 'product_url'
df['product_url']=product_links

# Scraping data like 'brand_name','product_name','number_of_reviews','love_count','star_rating'  and 'ingredients'
for each_product in range(len(df)):
    product_url = df['product_url'].iloc[each_product]
    product_content = extract_content(product_url)

    try:
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
        
    except:
        pass
    

# Scraping the remaining data like 'price', 'Fragrance Family','Scent Type','Key Notes' and 'Composition'
for each_product in range(len(data)):
    driver.get(df['product_url'].iloc[each_product])
    
    try:
        price(product_content)
    except:
        pass  
    
    
# Scraping the remaining data like 'Fragrance Family','Scent Type','Key Notes' and 'Composition'
for each_product in range(len(data)):
    driver.get(data['product_url'].iloc[each_product])
    
#Details
    try:
        driver.find_element_by_xpath('//*[@id="Details"]').click()
    except:
        pass
    time.sleep(3)
    try:
        Details(product_content)
    except:
        pass

    
#converting 'Details' TO A dictionary
for i in range(len(df)):
    dic={}
    while dic=={}:
        keys=[]
        values=[]
        for p in range(len(df['Details'].iloc[i])): 
            section=df['Details'].iloc[i][p]
            section=section.strip("''")
            split_section = section.split('\\n')
        #     print(split_section)
            
            for j in range(len(split_section)):
                if split_section[j]=='Composition':
                    keys.append(split_section[j])
                    values.append(split_section[j+1])


                if split_section[j]=='Fragrance Family':
                    keys.append(split_section[j])
                    values.append(split_section[j+1])


                if split_section[j]=='Key Notes':
                    keys.append(split_section[j])
                    values.append(split_section[j+1])

                if split_section[j]=='Features':
                    keys.append(split_section[j])
                    values.append(split_section[j+1])


                if split_section[j]=='Scent Type':
                    keys.append(split_section[j])
                    values.append(split_section[j+1])  
                    
        
                if (p==len(df['Details'].iloc[i])-1) and (j==len(split_section)-1) and (keys==[]):
                    dic=np.nan
     
            try:

                for l in range(len(keys)):
                    dic[keys[l]]=values[l]
            except:
                pass
            
    df['Details'][i]=dic
    
    
# extracting 'Fragrance Family','Scent Type','Key Notes' and 'Composition' data from Details Dictionary
for i in range(len(df)):
    try:
        df['Details'][i]=ast.literal_eval(df['Details'][i])
    except:
        pass
    
df=df[df['Details'].apply(lambda x: isinstance(x, dict))]

for i in range(len(df)):
    df['Fragrance Family'].iloc[i]=df['Details'].iloc[i].get('Fragrance_Family')

for i in range(len(df)):
    df['Scent_Type'].iloc[i]=df['Details'].iloc[i].get('Scent_Type')

for i in range(len(df)):
    df['Key_Notes'].iloc[i]=df['Details'].iloc[i].get('Key_Notes')    
    
for i in range(len(df)):
    df['Features'].iloc[i]=df['Details'].iloc[i].get('Features')

for i in range(len(df)):
    df['COMPOSITION'].iloc[i]=df['Details'].iloc[i].get('COMPOSITION')
    
# to print data
print(df)   





