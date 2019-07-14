from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)
    
def scrape():
    browser = init_browser()
    listings = {}

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    result = soup.find('li', class_='slide')
    # news_title = result.find(class_='content_title').text

    listings["news_title"] = result.find(class_='content_title').get_text()
    listings["news_description"] = result.find(class_= 'rollover_description_inner').get_text()
    

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/'
    browser.visit(image_url)
    time.sleep(3)
    image_html = browser.html
    soup = BeautifulSoup(image_html, 'html.parser')
    carousel = soup.find(class_='carousel_items')
    listings["featured_image_url"] = carousel.find(class_= 'button fancybox')['data-fancybox-href']
    
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(3)
    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')
    content = soup.find(class_='content')
    listings["mars_weather"] = content.find('p', class_ = 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    
  
    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts = {}
    mars_facts = pd.read_html(mars_facts_url)[1]
    mars_facts_html = mars_facts.to_html()
    listings["mars_facts"] = mars_facts_html
  
    # # Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(3)
    hemisphere_html = browser.html
    soup = BeautifulSoup(hemisphere_html, 'html.parser')
    image_links = soup.find_all('div', class_='description')
    
    full_urls = []
    full_links = []
    for image in image_links:
        image_url = image.find('a')['href']
        full_url = f'https://astrogeology.usgs.gov{image_url}'
        full_urls.append(full_url)
        browser.visit(full_url)
        time.sleep(3)
        image_html = browser.html
        soup = BeautifulSoup(image_html, 'html.parser')
        full_link = soup.find('img', class_='wide-image')['src']
        full_links.append(f'https://astrogeology.usgs.gov{full_link}')
        
    listings["full_url"] = full_urls
    listings["full_image_link"] = full_links
    print(listings)

    return listings
