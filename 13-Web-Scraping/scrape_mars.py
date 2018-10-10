# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# Function to scrape Mars data (from mission_to_mars.ipynb)
def scrape():

    # Initialize browser
    browser = init_browser()

    # Visit the NASA Mars News site
    mars_news_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news_url)

    # Scrape page into soup
    mars_news_html = browser.html
    mars_news_soup = BeautifulSoup(mars_news_html, 'html.parser')

	# Get title of latest news
    mars_news_results = mars_news_soup.find('li', class_="slide")
    mars_news_title = mars_news_results.find('h3').text

	# Get paragraph text of latest news
    mars_news_p = mars_news_results.find('div', class_="article_teaser_body").text

	# Now Visit the JPL Mars Space Images Site
    jpl_mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_mars_url)

	# Scrape page into soup
    jpl_mars_html = browser.html
    jpl_mars_soup = BeautifulSoup(jpl_mars_html, 'html.parser')

	# Do lots of manipulation to ultimately get full image URL of featured image
    jpl_mars_results = jpl_mars_soup.find('a', class_="button fancybox")
	#convert jpl_mars_results above into a string
    jpl_m_str = str(jpl_mars_results)
	#use split function and split on 'data-fancybox-href='
    jpl_m_str_split = jpl_m_str.split("data-fancybox-href=")
	#now we have a list so take the second element in that list
    new_jpl_str = jpl_m_str_split[1]
	#use split function again and split on " data-link"
    new_jpl_str_split = new_jpl_str.split(" data-link")
	#now we have a list so take the first element in that list to get the url we want but with a " as first element and last element
    new_img_str = new_jpl_str_split[0]
	# finally get the url we want but take out the " in front and end of the string
    final_img_str = new_img_str[1:-1]
	# now concatenate the base url value of https://www.jpl.nasa.gov to final_img_str to get featured_image_url
    featured_image_url = "https://www.jpl.nasa.gov" + final_img_str

	# Now visit Mars Weather Twitter account page
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)

	# Scape page into soup
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

	# Get the latest tweet with high, low, pressure and daylight info
    mars_weather_results = mars_weather_soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    sol_list = []
    for result in mars_weather_results:
        parsed_text_string = result.text
        if parsed_text_string[0:5] == "Sol 2":
            sol_list.append(parsed_text_string)

    mars_weather = sol_list[0]

	# Now visit the Mars Facts page
    mars_facts_url = 'https://space-facts.com/mars/'

	# Use read_html
    mars_facts_tables = pd.read_html(mars_facts_url)

	# Create a dataframe with column names Description and Value
    mars_facts_df = mars_facts_tables[0]
    mars_facts_df.columns = ['Description', 'Value']

	# Generate HTML table from dataframe
    mars_facts_html_table = mars_facts_df.to_html(index=False, justify='left')

	# Lastly visit the Mars Hemispheres page
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)

    # Scrape page into soup
    mars_hemispheres_html = browser.html
    mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')

	# results that we're looking for seem to be inside the <div class="description"
    mars_hemispheres_results = mars_hemispheres_soup.find_all('div', class_="description")

	# Create a list of all the hemisphere names
    hemisphere_title_list = []
    for result in mars_hemispheres_results:
        hemisphere_title = result.find('h3').text
        hemisphere_title_list.append(hemisphere_title)

	# Create a list of img_url
    hemisphere_img_url_list = []

    for item in hemisphere_title_list:
        # check if text of the hemisphere name from our list is shown on the screen and wait up to 2 seconds
        browser.is_text_present(item, 2)
        # click on link to go that specific hemisphere page
        browser.click_link_by_partial_text(item)
        #use BeautifulSoup to get html response
        enhanced_html = browser.html
        enhanced_soup = BeautifulSoup(enhanced_html, 'html.parser')
        #looks like the img url we're searching for is under <div class="downlaods">
        enhanced_results = enhanced_soup.find('div', class_= 'downloads')
        #then look under 'a' tag
        enhanced_link = enhanced_results.find('a')
        #then get full img url from href
        enhanced_href = enhanced_link['href']
        hemisphere_img_url_list.append(enhanced_href)
        # check if text 'Back' is shown on the screen (for back button) and wait up to 2 seconds
        browser.is_text_present('Back', 2)
        # click on the Back button to go back to previous page
        browser.click_link_by_partial_text('Back')

	# create four separate dictionaries, each with 'title' as first key and 'img_url' as second key
    first_dict = {'title': hemisphere_title_list[0], 'img_url': hemisphere_img_url_list[0]}
    second_dict = {'title': hemisphere_title_list[1], 'img_url': hemisphere_img_url_list[1]}
    third_dict = {'title': hemisphere_title_list[2], 'img_url': hemisphere_img_url_list[2]}
    fourth_dict = {'title': hemisphere_title_list[3], 'img_url': hemisphere_img_url_list[3]}

	# Create a list of the four dictionaries by using append function
    hemisphere_image_urls = []
    hemisphere_image_urls.append(first_dict)
    hemisphere_image_urls.append(second_dict)
    hemisphere_image_urls.append(third_dict)
    hemisphere_image_urls.append(fourth_dict)


	# Store everything scraped into one dictionary
    mars_results = {
    	"news_title": mars_news_title,
        "news_p": mars_news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_html_table": mars_facts_html_table,
        "hemisphere_image_urls": hemisphere_image_urls
        }

	# Return results
    return mars_results
