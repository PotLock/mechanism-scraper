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
service = Service(ChromeDriverManager().install())

# Initialize the WebDriver with Brave
driver = webdriver.Chrome(service=service, options=options)

# Open the website
driver.get("https://www.mechanisminsights.com/library/")

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

# Scrape the data
cards = driver.find_elements(By.CLASS_NAME, "css-1g4zz4p")
print(f"Number of cards detected: {len(cards)}")

data = []
for card in cards:
    title = card.find_element(By.CLASS_NAME, "css-5p1sze").text
    description = card.find_element(By.CLASS_NAME, "css-14uog0p").text
    link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
    data.append({"title": title, "description": description, "link": link})

# Save to CSV and JSON
df = pd.DataFrame(data)
df.to_csv("mechanism_institute_library.csv", index=False)

with open("mechanism_institute_library.json", "w") as f:
    json.dump(data, f, indent=4)

# Check if the number of detected cards matches the number of entries in JSON
if len(cards) == len(data):
    print(f"Success: The number of scraped entries ({len(data)}) matches the number of detected cards.")
else:
    print(f"Warning: The number of scraped entries ({len(data)}) does not match the number of detected cards ({len(cards)}).")

# Close the browser
driver.quit()
