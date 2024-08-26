import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Set up Brave browser
options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # Path to Brave

# Automatically manage the ChromeDriver version
# service = Service(ChromeDriverManager().install())

# Manually manage the ChromeDriver version by passing Brave compatible version in driver_version e.g. 127.0.6533.119
service = Service(ChromeDriverManager(driver_version="your_version_nubmer").install())

# Initialize the WebDriver with Brave
driver = webdriver.Chrome(service=service, options=options)

# Open the website
driver.get("https://www.mechanism.institute/library")

# Scroll to the bottom of the page to load all content
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for new content to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Wait for the page to fully load
time.sleep(2)

data = []

# Scrape the data
grid = driver.find_elements(By.CLASS_NAME, "grid") 

for container in grid:
    links = container.find_elements(By.TAG_NAME, "a")
    for li in links:
        link = (li.get_attribute("href"))
        title = li.find_element(By.CLASS_NAME, "text-xl").text
        description = li.find_element(By.CLASS_NAME, "text-sm").text
        tags_li = []
        tags = li.find_elements(By.TAG_NAME, "span")
        for tag in tags:
            tags_li.append(tag.text)
        data.append({"title": title, "description": description, "link": link, "tags": tags_li})

# Save to CSV and JSON
df = pd.DataFrame(data)
df.to_csv("mechanism_institute_library.csv", index=False)

with open("mechanism_institute_library.json", "w") as f:
    json.dump(data, f, indent=4)

# Check if the number of detected links matches the number of entries in JSON
if len(links) == len(data):
    print(f"Success: The number of scraped entries ({len(data)}) matches the number of detected cards.")
else:
    print(f"Warning: The number of scraped entries ({len(data)}) does not match the number of detected cards ({len(cards)}).")

# Close the browser
driver.quit()
