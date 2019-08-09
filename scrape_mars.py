from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    # Path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Grabbing the most recent news title and teaser from:
# "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

def scrape_news_info():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the news title & paragraph text

    news_title_div=soup.find('div', class_="content_title")
    news_teaser_div=soup.find('div', class_="article_teaser_body")
    
    # Get the text and store it
    title=news_title_div.text
    teaser=news_teaser_div.text

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return title, teaser

# JPL Mars Space Images - Featured Image from:
# https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars
def scrape_featured_image():
    browser = init_browser()

    # Visit:
    url = "https://www.jpl.nasa.gov"
    more_url = "/spaceimages/?search=&category=Mars"

    browser.visit(url+more_url)

    # Scrape page into Soup
    img_page_html = browser.html
    img_soup = bs(img_page_html, "html.parser")

    browser.quit()

    image_anchor = img_soup.find('a', {'class': 'button fancybox'})
    featured_img_url = image_anchor['data-fancybox-href']
    featured_img_url = f'{url}{featured_img_url}'
    return featured_img_url

# Mars Weather Report from:
# https://twitter.com/MarsWxReport
def scrape_weather_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get to the tweets
    weather_span=soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    # Quite the browser after scraping
    browser.quit()

    tweets=[]
    for tweet in weather_span:
        tweets.append(tweet.text)

    temp_tweets = [tweet for tweet in tweets if "InSight" in tweet and "low" in tweet and "high" in tweet]
    mars_weather = temp_tweets[0]
    return mars_weather

# Mars Facts from:
# https://space-facts.com/mars/
def scrape_mars_facts():

    browser = init_browser()

    # Visit website
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get to the table, pull categories and facts
    mars_fact_categories=soup.find('table', {'class':"tablepress tablepress-id-p-mars"}).find('tbody').find_all('td',{'class':'column-1'})
    mars_facts=soup.find('table', {'class':"tablepress tablepress-id-p-mars"}).find('tbody').find_all('td',{'class':'column-2'})

    # Get the text by itself:
    categories=[]
    for fact in mars_fact_categories:
        categories.append(fact.text)
    facts=[]
    for fact in mars_facts:
        facts.append(fact.text)

    # Quite the browser after scraping
    browser.quit()

    mars_facts_dict= dict(zip(categories,facts))

    mars_series = pd.Series(mars_facts_dict)
    mars_df = pd.DataFrame(mars_series)
    mars_table = mars_df.to_html()

    return mars_table


# Mars Hemispheres images from:
# https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars

def scrape_full_res_images():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #get to the current featured image

    product_images = soup.find('div',class_="collapsible results")
    image_data=product_images.find_all('div',class_='item')

    results = []
    for image in image_data:
        results.append(image.text)

    titles=[]
    for result in results:
        titles.append(result.split('Enhanced')[0][:-1])

    hemisphere_image_results = []
    for title in titles:
        browser.click_link_by_partial_text(title)
        img_html = browser.html
        img_soup = bs(img_html, "html.parser")
        img_url = img_soup.find('div',class_='downloads').find('ul').find('li')
        tif_url = str(img_url.find('a'))
        tif_url = tif_url.split('=')[1].split(' ')[0].replace('"', '')
        hemisphere_image_results.append({'title':title,'img_url':tif_url})
        
        browser.back()

    browser.quit()

    return hemisphere_image_results