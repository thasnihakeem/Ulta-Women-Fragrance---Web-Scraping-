
import time
import random
import warnings
import pandas as pd
from typing import List
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
    brand = dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/h1/span[1]/a/text()')
    if not brand:
        brand = 'brand is not available'
    else:
        brand = re.sub('[\[\]\']', '', str(brand))
    df['Brand'].iloc[each_product] = brand
    return brand

def Product_name(dom):
    product = dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/h1/span[2]/text()')
    if product:
        product = re.sub(r'[\[\]\'\"]', '', str(product))
        df.loc[each_product, "Product_name"] = product
    else:
        df.loc[each_product, "Product_name"] = "Product name is not available"
    return product

def Reviews(dom):
    number_of_reviews = dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/div/span[2]/text()')
    if number_of_reviews:
        number_of_reviews = re.sub(r'[\,\(\)\[\]\'\"]', '', str(number_of_reviews))
        df.loc[each_product, "Number_of_reviews"] = number_of_reviews
    else:
        df.loc[each_product, "Number_of_reviews"] = "Number of reviews is not available"
    return number_of_reviews

def Star_Rating(dom):
    star_rating = dom.xpath('//*[@id="92384e5c-2234-4e8f-bef7-e80391889cfc"]/div/a/span/text()')
    if star_rating:
        star_rating = re.sub(r'[\,\(\)\[\]\'\"\ Q & A\ Ask A Question]', '', str(star_rating))
        df.loc[each_product, "Star_rating"] = star_rating
    else:
        df.loc[each_product, "Star_rating"] = "Star rating is not available"
    return star_rating

def Ingredients(dom):
    ingredients = dom.xpath("//*[@aria-controls='Ingredients']//p/text()")
    if ingredients:
        ingredients = re.sub(r'[\[\]\']', '', str(ingredients))
        df.loc[each_product, "Ingredients"] = ingredients
    else:
        df.loc[each_product, "Ingredients"] = "Ingredients is not available"
    return ingredients

def Fragrance_Description():
    element = driver.find_element("xpath", '//*[@id="b46bc3ad-9907-43a6-9a95-88c160f02d7f"]/p')
    if element:
        description = element.text
        description = re.sub(r'[\[\]]', '', description)
    else:
        description = "Fragrance description is not available"
    return description

def Price():
    prices = driver.find_element("xpath",'//*[@id="1b7a3ab3-2765-4ee2-8367-c8a0e7230fa4"]/span').text
    if prices:
        prices = re.sub(r'[\$\,\(\)\[\]\'\"]', '', prices)
    else:
        prices="Price is not available"
    return prices
                        
def Detail():
    try:                                                                                
        driver.find_element("xpath",'//*[@id="Details"]').click()                     
    except:                                                                              
        pass
    time.sleep(3)                       
    details = driver.find_element("xpath", "//*[@aria-controls='Details']").text
    if details:
        return details
    else:
        return "Details are not available"
    return Details

# Creating a dictionary of the required columns
data = {
    'Product_url': [], 
    'Brand': [], 
    'Product_name': [],
    'Number_of_reviews': [],
    'Details': [], 
    'Star_rating': [],
    'Price': [], 
    'Fragrance Description': [],
    'Ingredients': []
}
# Creating a dataframe with those columns
df = pd.DataFrame(data)
# Assigning the scraped links to the column 'product_url'
df['Product_url']=product_links

def get_page_urls(url):
    page_urls = [url]
    while url:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        next_page = soup.find('li', class_='next-prev floatl-span').find('a', class_='next')
        if next_page:
            url = "https://www.ulta.com" + next_page['href']
            page_urls.append(url)
        else:
            url = None
    driver.quit()
    return set(page_urls)

url = "https://www.ulta.com/womens-fragrance?N=26wn"
page_urls = get_page_urls(url)

# Fetching all resulted product links
def get_product_links(page_urls: List[str]) -> List[str]:
    product_links = []
    for url in page_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = ["https://www.ulta.com" + row.a['href'] for row in soup.find_all('p', class_='prod-desc')]
        product_links.extend(links)
    return product_links

product_links = get_product_links(page_urls)

# Indicate scraping completion
print("Got All Product Links! There are {} products in total.".format(len(product_links)))

count=0
for each_product in range(len(df)):
    count+=1
    product_url = df['Product_url'].iloc[each_product]
    product_content = extract_content(product_url)
    Brand(product_content)
    Product_name(product_content)
    Reviews(product_content) 
    Star_Rating(product_content)                       
    Ingredients(product_content) 
    print('{}done'.format(count))

count=0
for each_product in range(len(df)):
    count+=1
    driver.get(df['Product_url'].iloc[each_product])               
   
    price=Price()                                                                 
    df["Price"].iloc[each_product]= price                                       
    
    fragrance_description=Fragrance_Description()                                   
    df['Fragrance Description'].iloc[each_product] = fragrance_description          
    
    details=Detail()                                                                
    df['Details'].iloc[each_product] = details                                     

    pz=None
    dt=None
    print('{} done'.format(count
                          ))

# to print data
print(df) 

# Convering data to a csv file
df.to_csv("Ulta_Women_Fragrance_Data")

