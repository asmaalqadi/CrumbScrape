from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import random

# Setup Selenium with headless Chrome to run browser in the background
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--no-sandbox')  # Disable sandboxing for Chrome (useful for certain environments)

# Create a new instance of the Chrome driver using webdriver-manager to handle driver installation
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Prompt user for inputting a number to correspond to food options
user_choice = int(input("1. Cupcakes\n2. Cakes\n3. Cookies\n4. Candy\n5. Breads\nEnter a number for what recipes you'd like: "))

# Map the number inputted to different recipe categories on the website
choice_map = {1: 'cupcakes', 2: 'cakes', 3: 'cookies', 4: 'candy', 5: 'breads'}
choice = choice_map[user_choice] 

# Create the url using the choice based on user input
url = f'https://preppykitchen.com/category/recipes/desserts/{choice}/'

# Fetch the webpage content using Selenium 
driver.get(url)

# Get the complete HTML content of the page after all scripts are executed
html = driver.page_source

# Close the browser once the content is fetched
driver.quit()

# Parse the page content with BeautifulSoup to extract desired information
soup = BeautifulSoup(html, 'html.parser')

# Find all the article tags with the specified class name
articles = soup.find_all('article', class_='simple-grid')

# If no articles were found, print an error message
if not articles:
    print("No recipes found for this category.")
else:
    # If articles are found, collect recipe titles and links
    recipe_info = []
    for article in articles:
        title_tag = article.find('h2', class_='entry-title')  # Locate the title tag within the article
        if title_tag:
            title = title_tag.get_text(strip=True)  # Extract text of the title
            link = title_tag.find('a')['href']  # Extract link 
            recipe_info.append((title, link))  # Store the title and link in a list

    # Select up to 5 random recipes from the list of found recipes
    random_info = random.sample(recipe_info, min(5, len(recipe_info)))

    # Print the selected recipe names and their corresponding links
    for title, link in random_info:
        print(f"Title: {title}")
        print(f"Link: {link}")
        print('-' * 40)


