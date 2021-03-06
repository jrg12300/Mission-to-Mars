# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
executable_path = {'executable_path': '../chromedriver.exe'}
browser = Browser('chrome', executable_path, headless=False)



def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None,None

    return news_title,news_p

def featured_image(browser):
    # ### Featured Images
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    img_soup = soup(browser.html, 'html.parser')
    try:
        #Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None    
    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    return img_url

def mars_facts():
    try:
        df = pd.read_html('http://space-facts.com/mars/')[0]
        #browser.quit()
    except BaseException:
        return None
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)    
    return df.to_html()

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    } 
    # Stop webdriver and return data
    browser.quit()
    return data


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())



