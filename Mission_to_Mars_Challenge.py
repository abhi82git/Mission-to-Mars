#!/usr/bin/env python
# coding: utf-8

# ### News Title and Summary

# In[148]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[149]:


# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)


# In[23]:


# Visit the Mars news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[24]:


# Convert the browser html to a soup object and then quit the browserhtml = browser.html
html = browser.html
news_soup = soup(html,'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[25]:


news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[26]:


news_summary = slide_elem.find('div', class_='article_teaser_body').get_text()
news_summary


# ### Featured Images

# In[27]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[28]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[29]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[30]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[31]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[32]:


#df = pd.read_html('https://galaxyfacts-mars.com')[0]
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns = ['description','Mars','Earth']
df.set_index('description', inplace=True)


# In[33]:


df


# In[34]:


df.to_html()


# ### D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# In[150]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[151]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
mars_home_page_url = 'https://marshemispheres.com/index.html'

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hemi_soup = soup(html,'html.parser')
hemi_box = hemi_soup.find_all('div', class_='description')

for hemi in hemi_box:
    link_text = hemi.find('h3')
    img_page = browser.find_by_text(link_text.text)
    img_page.click()
    img_html = browser.html
    img_soup = soup(img_html,'html.parser')
    img_rel_url = img_soup.find('li').find('a').get('href')
    img_full_url = f'{mars_home_page_url}/{img_rel_url}'
    title = img_soup.find('h2', class_='title').get_text()
    hemi_dict = {'img_url': img_full_url, 'title': title}
    hemisphere_image_urls.append(hemi_dict)
    browser.back()



    


# In[152]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[153]:


# 5. Quit the browser
browser.quit()


# In[ ]:




