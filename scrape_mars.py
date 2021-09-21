import pymongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # return browser
    # browser = init_browser()

    # NASA Mars News
    newsUrl = 'https://redplanetscience.com/'
    browser.visit(newsUrl)
    browser.is_element_present_by_css('div.list_text', wait_time=2)
    html = browser.html

    newsSoup = bs(html, 'html.parser')

        # news_title
    div_level = newsSoup.select_one('div.list_text')
    div_level.find('div', class_='content_title')
    news_title = div_level.find('div', class_='content_title').text

        #news_p
    div_level = newsSoup.select_one('div.list_text')
    div_level.find('div', class_='article_teaser_body')
    news_p = div_level.find('div', class_='article_teaser_body').text

    # Mars images
    imageUrl = 'https://spaceimages-mars.com/'
    browser.visit(imageUrl)
    fullImage = browser.find_by_tag("button")[1]
    fullImage.click()
    html = browser.html
    imageSoup = bs(html, 'html.parser')
    image_src = imageSoup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = 'https://spaceimages-mars.com/' + image_src

    # Mars facts
    factsUrl = 'https://galaxyfacts-mars.com/'
    factTables = pd.read_html(factsUrl)
    mars_df = factTables[0]
    mars_df = mars_df.drop(columns=2)
    mars_df.at[0,0] = 'Name'
    mars_facts_html = mars_df.to_html()

    # Mars Hemispheres
    hemisphereUrl = 'https://marshemispheres.com/'
    browser.visit(hemisphereUrl)
    time.sleep(3)
    html = browser.html
    hemisphereSoup = bs(html, 'html.parser')
    
    hemisphere_image_url = []
    links = browser.find_by_css('a.itemLink img')
    for link in range(len(links)):
        hemisphere_image_dict = {}
        browser.find_by_css('a.itemLink img')[link].click()
        imageUrl = browser.find_by_text("Sample").first
        hemisphere_image_dict["img_url"] = imageUrl["href"]
        title = browser.find_by_css('h2.title').text
        hemisphere_image_dict["title"] = title
        hemisphere_image_url.append(hemisphere_image_dict)
        browser.back()
    hemisphere_image_url
    # Create the dictionary
    mars_dictionary = {
        'Latest_News': news_title,
        'News_Summary': news_p,
        'Featured_Image': featured_image_url,
        'Facts': mars_facts_html,
        'Hemisphere_Images': hemisphere_image_url
    }


    # Quit the browser
    browser.quit()

    # Return the results
    return mars_dictionary