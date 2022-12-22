# Importing libraries
import time
import random
import warnings
import pandas as pd
from lxml import etree as et
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
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

def Brand(dom):
    try:                                                                                           #try to get the data
        brand=(dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/h1/span[1]/a/text()'))   #get the Brand name of the listing
        df['Brand'].iloc[each_product] = brand                                                     #To add data to a column
        df[['Brand']] = df[['Brand']].astype(str)                                                  #converting to string
        df['Brand'] = df['Brand'].str.replace('[','')                                              #Removing unwanted characters
        df['Brand'] = df['Brand'].str.replace(']','')
        df['Brand'] = df['Brand'].str.replace("'",'')
    except:                                                                                        #if the brand is not found, print the error message
        brand = "brand is not available"
        df['Brand'].iloc[each_product] = brand   
    return  brand

def Product(dom):
    try:                                                                                            #try to get the data
        product=(dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/h1/span[2]/text()'))    #get the Product name of the listing
        df['Product_name'].iloc[each_product] = product                                             #To add data to a column
        df[['Product_name']] = df[['Product_name']].astype(str)                                     #converting to string
        df['Product_name'] = df['Product_name'].str.replace('[','')                                 #Removing unwanted characters
        df['Product_name'] = df['Product_name'].str.replace(']','')
        df['Product_name'] = df['Product_name'].str.replace("'",'')
        df['Product_name'] = df['Product_name'].str.replace('"','')
    except:                                                                                         #if the product_name is not found, print the error message
        product = "product_name is not available"
        df['Product_name'].iloc[each_product] = product   
    return  product

def Reviews(dom):
    try:                                                                                                       #try to get the data
        number_of_reviews=(dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/div/span[2]/text()'))    #get the number_of_reviews of the listing
        df['Number_of_reviews'].iloc[each_product] = number_of_reviews                                         #To add data to a column
        df[['Number_of_reviews']] = df[['number_of_reviews']].astype(str)                                      #converting to string
        df['Number_of_reviews'] = df['Number_of_reviews'].str.replace(',','')                                  #Removing unwanted characters
        df['Number_of_reviews'] = df['Number_of_reviews'].str.replace('(','')
        df['Number_of_reviews'] = df['Number_of_reviews'].str.replace(')','')
        df['Number_of_reviews'] = df['Number_of_reviews'].str.replace('[','')
        df['Number_of_reviews'] = df['Number_of_reviews'].str.replace(']','')
        df['Number_of_reviews'] = df['Number_of_reviews'].str.replace("'size:'",'')
        df['Number_of_reviews'] = df['Number_of_reviews'].str.replace("'",'')
    except:                                                                                                     #if the number_of_reviews is not found, print the error message                                       
        number_of_reviews = "number_of_reviews is not available"
        df['Number_of_reviews'].iloc[each_product] = number_of_reviews   
    return  number_of_reviews

def Star_rating(dom):
    try:                                                                                                 #try to get the data
        star_rating=(dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/div/a/span/text()'))     #get the star_rating of the listing
        df['Star_rating'].iloc[each_product] = star_rating                                               #To add data to a column
        df[['Star_rating']] = df[['Star_rating']].astype(str)                                            #converting to string
        df['Star_rating'] = df['Star_rating'].str.replace(']','')                                        #Removing unwanted characters
        df['Star_rating'] = df['Star_rating'].str.replace('[','')
        df['Star_rating'] = df['Star_rating'].str.replace('Q & A','')
    except:                                                                                             #if the star_rating is not found, print the error message 
        star_rating = "star_rating is not available"
        df['Star_rating'].iloc[each_product] = star_rating   
    return  star_rating

def Price():
    try:                                                                                                    #try to get the data
        Prices=driver.find_element(By.XPATH,'//*[@id="1b7a3ab3-2765-4ee2-8367-c8a0e7230fa4"]/span').text    #get the Price of the listing
        Prices = str(Prices)                                                                                #converting to string
        Prices = Prices.replace('[','')                                                                     #Removing unwanted characters
        Prices = Prices.replace(']','')
        Prices = Prices.replace('$','')
        Prices = Prices.replace("'",'')
    except:                                                                                                 #if the Price is not found, print the error message
        Prices = "Price is not available" 
    return Prices

def Ingredients(dom):
    try:                                                                                         #try to get the data
        ingredients=ingredients=(dom.xpath("//*[@aria-controls='Ingredients']//p/text()"))       #get the Ingredients of the listing
        df['Ingredients'].iloc[each_product] = ingredients                                       #To add data to a column 
        df[['Ingredients']] = df[['Ingredients']].astype(str)                                    #converting to string
        df['Ingredients'] = df['Ingredients'].str.replace('[','')                                #Removing unwanted characters
        df['Ingredients'] = df['Ingredients'].str.replace(']','')
    except:                                                                                      #if the Ingredients is not found, print the error message 
        ingredients = "Ingredients is not available"
        df['Ingredients'].iloc[each_product] = ingredients   
    return  ingredients
    
def Fragrance_Description():
    try:                                                                                                                #try to get the data
        Fragrance_Descriptions=driver.find_element(By.XPATH,'//*[@id="b46bc3ad-9907-43a6-9a95-88c160f02d7f"]/p').text   #get the Fragrance_Description of the listing
        Fragrance_Descriptions = str(Fragrance_Descriptions)                                                            #converting to string
        Fragrance_Descriptions = Fragrance_Descriptions.replace('[','')                                                 #Removing unwanted characters
        Fragrance_Descriptions = Fragrance_Descriptions.replace(']','')
    except:                                                                                                             #if the Fragrance_Description is not found, print the error message 
        Fragrance_Descriptions = "Fragrance_Description is not available" 
    return Fragrance_Descriptions

def Detail():
    try:                                                                                   #try to get '+' button
        driver.find_element(By.XPATH,'//*[@id="Details"]').click()                         #to click the '+' button of the in the site to get the details data
    except:                                                                                #to pass it ,if '+' button can't be located
        pass
    time.sleep(3)
    try:                                                                                   #try to get the data
        Details = driver.find_element(By.XPATH, "//*[@aria-controls='Details']").text      #get the Details of the listing                                                                        #To add data to a column
    except:                                                                                #if the Details is not found, print the error message
        Details = "Details is not available"
    return Details                                                                                 

# Ulta website link
URL="https://www.ulta.com/womens-fragrance?N=26wn"

#list to store the url of every resultant page
base_url_link = [URL]   #list of base url
while URL!=[]:
    driver.get(URL)
    response = driver.page_source
    soup = BeautifulSoup(response , 'html.parser')
    for all_pages in soup.find_all('li', class_="next-prev floatl-span"):   #get the all resultant page url of the listing
        x=all_pages.find('a',class_='next')
        if x:
            a="https://www.ulta.com" + x['href']                            #converting to valid url
            base_url_link.append("https://www.ulta.com" + x['href'])        #storing all rasultant page link in a list   
            URL=a

        else:
            URL=[] 
base_url_links=set(base_url_link)                                           # converting base_url_link to set to get unique values        
page_lst_link=list(base_url_links)                                          # converting to list

# Fetching all resulted product links
product_links = []
for each_page_link in  page_lst_link:
    driver.get(each_page_link)
    response = driver.page_source
    soup = BeautifulSoup(response , 'html.parser')
    for row in soup.find_all('p', class_='prod-desc'):                           #get the all resultant product url of the listing
        main_box=(row.a['href'])
    for row in soup.find_all('p', class_='prod-desc'):
        product_links.append("https://www.ulta.com" + row.a['href'])             #converting to valid url  and storing it in a list

# Indicate scraping completion
print(f'Got All Brand Links! There are {len(product_links)} brands in total.')

# Creating a dictionary of the required columns
data_dic = {'Product_url': [], 'Brand': [], 'Product_name': [],'Number_of_reviews': [], 
            'Details': [], 'Star_rating': [],'Price':[], 'Fragrance Description':[],'Ingredients':[]}

# Creating a dataframe with those columns
df=pd.DataFrame(data_dic)

# Assigning the scraped links to the column 'product_url'
df['Product_url']=product_links

# Scraping data like 'brand_name','product_name','number_of_reviews','love_count','star_rating'  and 'ingredients'
for each_product in range(len(df)):
    product_url = df['Product_url'].iloc[each_product]
    product_content = extract_content(product_url)
    Brand(product_content)                                 # brands
    Product(product_content)                               # product_name
    Reviews(product_content)                               # number_of_review
    Star_rating(product_content)                           # star_rating
    Ingredients(product_content)                           #ingredients
    
# Scraping 'price' ,'Fragrance Description' and 'Details' data
for each_product in range(len(df)):
    driver.get(df['Product_url'].iloc[each_product])               
    price=Price()                                                                   #Price
    df["Price"].iloc[each_product]= price                                           #To add data to a column

    fragrance_description=Fragrance_Description()                                   #Fragrance Description
    df['Fragrance Description'].iloc[each_product] = fragrance_description          #To add data to a column
 
    details=Detail()                                                                #Details
    df['Details'].iloc[each_product] = details                                      #To add data to a column

    pz=None
    dt=None     
    
# to print data
print(df) 

# Convering data to a csv file
df.to_csv("Ulta_Women_Fragrance_Data")
