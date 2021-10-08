# #### import Splinter and BeautifulSoup
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# #### set executable path
xecutable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# #### assign the url and instruct the browser to visit it
## 1. searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list 
##    would be found in HTML as <ul class="item_list">.
## 2. Secondly, we're also telling our browser to wait one second before searching for components. The optional delay is 
##    useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy.

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# #### set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Get article summary
art_summ = slide_elem.find('div', class_='article_teaser_body').get_text()
art_summ


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

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# Get the infor from a table 
df = pd.read_html('https://galaxyfacts-mars.com')[0] #index '0' means - get the first table
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()