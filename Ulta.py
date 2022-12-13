import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import random
import json
from unidecode import unidecode
import pandas as pd
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
links=[]
band_lst_link=["https://www.ulta.com/womens-fragrance?N=26wn&No=0&Nrpp=96","https://www.ulta.com/womens-fragrance?N=26wn&No=96&Nrpp=96","https://www.ulta.com/womens-fragrance?N=26wn&No=192&Nrpp=96","https://www.ulta.com/womens-fragrance?N=26wn&No=288&Nrpp=96","https://www.ulta.com/womens-fragrance?N=26wn&No=384&Nrpp=96","https://www.ulta.com/womens-fragrance?N=26wn&No=480&Nrpp=96"]
for i in band_lst_link:
    response = requests.get(i)
    # Use BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    for row in soup.find_all('p', class_='prod-desc'):
        #     prod={}
        main_box = (row.a['href'])

    for row in soup.find_all('p', class_='prod-desc'):
        links.append("https://www.ulta.com" +
                     row.a['href'])

with open('links.txt', 'w') as f:
    for item in links:
        f.write(f"{item}\n")

# Indicate scraping completion
print(f'Got All Brand Links! There are {len(links)} brands in total.')

data_dic = {'product_url': [], 'brand': [], 'product_name': [], 'number_of_reviews': [], 'star_rating': [], 'price': [],
            'Details': [], 'Fragrance Family': [], 'Scent Type': [], 'Key Notes': [], 'Fragrance Description': [],
            'COMPOSITION': [], 'Ingredients': []}

df = pd.DataFrame(data_dic)

# pd.Index.size!=len(link)
df['product_url'] = links

for i in range(len(df)):
    response = requests.get(df['product_url'].iloc[i])
    my_url = df['product_url'].iloc[i]
    My_url = ureq(my_url)
    my_html = My_url.read()
    My_url.close()
    soup = BeautifulSoup(my_html, 'html.parser')
    dom = et.HTML(str(soup))
    # brands
    brand = (dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/h1/span[1]/a/text()'))
    df['brand'].iloc[i] = brand
    # product_name
    product = (dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/h1/span[2]/text()'))
    df['product_name'].iloc[i] = product
    # number_of_reviews
    try:
        number_of_reviews = (dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/div/span[2]/text()'))
        df['number_of_reviews'].iloc[i] = number_of_reviews
    except:
        pass
    # star_rating
    try:
        star_rating = (dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/div/a/span/text()'))
        df['star_rating'].iloc[i] = star_rating
    except:
        pass
    # price
    try:
        price = (dom.xpath('//*[@id="1b7a3ab3-2765-4ee2-8367-c8a0e7230fa4"]/span/text()'))
        df['price'].iloc[i] = price
    except:
        pass

    # Ingredients
    try:
        Ingredients = (
            dom.xpath('//*[@id="bb5f7945-7101-402b-b8b3-1ad025315d50"]/div/div/details[3]/div/div/p[1]/text()'))
        df['Ingredients'].iloc[i] = Ingredients
    except:
        pass

    # Fragrance Description
    try:
        Fragrance_Description = (dom.xpath('//*[@id="b46bc3ad-9907-43a6-9a95-88c160f02d7f"]/p/text()'))
        df['Fragrance Description'].iloc[i] = Fragrance_Description
    except:
        pass
    # Details
    try:
        Details = (dom.xpath('//*[@id="bb5f7945-7101-402b-b8b3-1ad025315d50"]/div/div/details[3]/text()'))
        df['Details'].iloc[i] = Details
    except:
        pass

df

df.to_csv("v")
