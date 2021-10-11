# #### import Splinter and BeautifulSoup
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

#############################
def scrape_all():
    # #### set executable path
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
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
    # Signal that the function is complete
    return data

#############################
# #### assign the url and instruct the browser to visit it
## 1. searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list 
##    would be found in HTML as <ul class="item_list">.
## 2. Secondly, we're also telling our browser to wait one second before searching for components. The optional delay is 
##    useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    # #### set up the HTML parser:
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling 
    # (if scrapping web page's format has changed)
    # In case the any errors during scrapping, continue with
    #other scraping portions, even if it doesn't work...
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Get article summary
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p

#############################
def featured_image(browser):
    # ### Featured Images
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

#############################
def mars_facts():
    # ### Mars Facts
    # Get the infor from a table 
    # use 'read_html" to scrape the facts table into a dataframe
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0] #index '0' means - get the first table
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

#############################
# Instruct FLASK to run
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())