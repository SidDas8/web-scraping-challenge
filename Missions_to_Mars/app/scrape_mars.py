# Import dependencies
import requests
import pandas as pd
import pymongo
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    
    # Mars News
    # Set up the Mars News Site to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # Scrape news title and news paragraph text
    newstitle = soup.find('div', class_='content_title').text
    paragraphtext = soup.find('div', class_='article_teaser_body').text
    
    
    # JPL Mars Space Images - Featured Image
    
    # Set up the Mars Space image to be scraped
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)

    # Click on button to see full size image
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # Create BeautifulSoup object; parse with 'html.parser'
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    
    # Scrape full size image url
    imageurl = soup2.find('img', class_='fancybox-image')['src']

    # Concatenate complete url
    featuredimageurl = url2 + imageurl    
    
    
    # Mars Facts
    # URL for Mars Facts table
    url3 = 'https://galaxyfacts-mars.com/'

    # Use pandas to read html file
    factstables = pd.read_html(url3)

    # Table with Mars planet facts
    marstable = factstables[1]
    
    # Use pandas to convert the data to a HTML table string
    htmltable = marstable.to_html()
    

    # Mars Hemispheres
    # Set up the Mars Hemispheres images to be scraped
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

    # Create BeautifulSoup object; parse with 'html.parser'
    html4 = browser.html
    soup4 = bs(html4, 'html.parser')
    
    # Find the 'item' class for each hemisphere
    classitems = soup4.find_all('div', class_='item')

    # Lists for HTML scrape
    hemisphere_url_list = []
    title_list = []

    # Loop through the 4 'item' classes
    for hemisphere in classitems:

        # Scrape the link for each hemisphere website
        img_url = hemisphere.find('a')['href']
        hemisphere_url_list.append(url4 + img_url)

        # Scrape the title for each hemisphere
        title_list.append(hemisphere.find('h3').text)
    
    # Create list of dictionaries for hemisphere titles and image urls
    hemisphere_data = []

    # Append dictionaries to list using loop
    for each in range(len(hemispheres)):
        hemisphere_data.append({"title": title_list[each], "fullsize_url": fullsize_img_urls[each]})
    
        
    # Store Mars data in a dictionary
    mars_data_dictionary = {
        "news_title": newstitle,
        "paragraph_text": paragraphtext,
        "featured_image_url": featuredimageurl,
        "html_table": htmltable,
        "hemisphere_data": hemisphere_data
    }
    
    # Close the browser after scraping
    browser.quit()
    
    return mars_data_dictionary