# Import Splinter and BeautifulSoup and Pandas
from pandas.io import html
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# define function 
def scrape_all():
    # Initiate headless driver for deployment
    # set up executable path and URL for scraping
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in the dictionary
    data = {
        "news_title": news_title, 
        "news_paragraph": news_paragraph, 
        "featured_image": featured_image(browser), 
        "hemispheres": hemisphere(),
        "facts": mars_facts(), 
        "last_modified": dt.datetime.now()
    }

    # Step webdriver and return data
    browser.quit()
    return data

# Add the function 
def mars_news(browser):

    # assign the URL and instruct the browser to visit the Mars NASA news site
    # url = "https://data-class-mars.s3.amazonaws.com/Mars/index.html"
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("div.list_text", wait_time = 1)

    # set up HTML parser
    html = browser.html
    news_soup = soup(html, "html.parser")
    
    # Add try/except for error handling
    try:

        # Scraping
        slide_elem = news_soup.select_one("div.list_text")
        # Use the parent element to find the first "a" tag and save it as "new_title"
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

# Declare and define function 
def featured_image(browser):

    # Setup URL to visit
    # url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag("button")[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html 
    img_soup = soup(html, "html.parser")

    # Add try except for Error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find("img", class_="fancybox-image").get("src")
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f"https://spaceimages-mars.com/{img_url_rel}"

    return img_url

# ### Mars Facts

# add function 
def mars_facts():

    # Try/Except for error handling with BaseException
    try:
        # Setup the code to scrape the entire table with Pandas 
        df = pd.read_html("https://galaxyfacts-mars.com")[0]
    
    except BaseException:
        return None

    df.columns= ["Description", "Mars", "Earth"]
    df.set_index("Description", inplace=True)

    # convert back DataFrame to html using .to_html()
    return df.to_html(classes="table table-striped")

def hemisphere():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []
    
    for x in range(4):
        browser.find_by_css("a.product-item img")[x].click()
        hemisphere_data = soup(browser.html, "html.parser")

        
        image_path = hemisphere_data.find("ul")
        image = image_path.find("a", target="_blank").get("href")
        title = hemisphere_data.find("h2").text

        hemisphere = {
            "img_url":url + image,
            "title": title}
        
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data 
    print(scrape_all())




