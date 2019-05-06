
# Declare Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import datetime as dt


# NASA Mars News
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #get first list item and wait half a second if not immediately present
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=0.5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser') 
    try:
    
        news_title = soup.find('div', class_= 'content_title').find('a').text

        news_p = soup.find('div', class_= 'article_teaser_body').text
       
    except AttributeError:
        return None, None
    return news_title, news_p


# JPL Mars Space Images - Featured Image

def featured_image(browser):   
    url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Asking splinter to go to the site hit a button with id name full_image
    # Find the image url for the current Featured Mars Image
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_element = browser.find_link_by_partial_text('more info')
    more_info_element.click()

    # Parse the results html with soup
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')
    
    img = image_soup.select_one('figure.lede a img')
    try:
        img_url = img.get('src')
    except AttributeError:
        return None
    # Use the base url to create an absolute url
    featured_image_url = f'https://www.jpl.nasa.gov{img_url}'
    return featured_image_url 



# Mars Weather
def twitter_weather(browser):
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    mars_weather_tweet = weather_soup.find('div',
                                      attrs={"class":"tweet",
                                            "data-name":"Mars Weather"})


    mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
    return mars_weather

# Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None
    #Create Columns' names
    df.columns = ['Description','Value']

    #Reset index
    df.set_index('Description', inplace=True)
    facts = df.to_html(classes= "table table-striped") 
    return facts

# Mars Hemispheres
def hemisphere(browser):
    try:
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')
        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemisphere_urls = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link that leads to full image website
            img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(hemispheres_main_url + img_url)
            
            # HTML Object of individual hemisphere information website 
            img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( img_html, 'html.parser')
            
            # Retrieve full image source 
            full_img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemisphere_urls.append({"title" : title, "img_url" : full_img_url})
        return hemisphere_urls
    finally:
        browser.quit()


# main bot
def scrape_all():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    featured_image_urls = featured_image(browser)
    mars_weather = twitter_weather(browser)
    hemisphere_urls = hemisphere(browser)
    facts = mars_facts()
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image":featured_image_urls,
        "hemispheres": hemisphere_urls,
        "weather": mars_weather,
        "facts": facts,
        "last_modified": timestamp 
    }
    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape_all())


