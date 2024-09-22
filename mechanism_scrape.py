import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def load_page():
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

def scrape_links():
    data = []

    grid = driver.find_elements(By.CLASS_NAME, "grid") 

    for container in grid:
        links = container.find_elements(By.TAG_NAME, "a")
        for li in links:
            link = (li.get_attribute("href"))
            data.append({"link": link})
    return data


# Set up Brave browser
options = webdriver.ChromeOptions()
options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"  # Path to Brave

# Automatically manage the ChromeDriver version
service = Service(ChromeDriverManager().install())

# Manually manage the ChromeDriver version by passing Brave compatible version in driver_version e.g. 127.0.6533.119
#service = Service(ChromeDriverManager(driver_version="your_version_number").install())

# Initialize the WebDriver with Brave
driver = webdriver.Chrome(service=service, options=options)

# Open the website
driver.get("https://www.mechanism.institute/library")

# Scroll to the bottom of the page to load all content
load_page()

# Scrape the links
data = scrape_links()

#initializing new data list
data2 = []
# grid = driver.find_elements(By.CLASS_NAME, "grid") 

# for container in grid:
#     links = container.find_elements(By.TAG_NAME, "a")
#     for li in links:
#         link = (li.get_attribute("href"))
#         title = li.find_element(By.CLASS_NAME, "text-xl").text
#         description = li.find_element(By.CLASS_NAME, "text-sm").text
#         tags_li = []
#         tags = li.find_elements(By.TAG_NAME, "span")
#         for tag in tags:
#             tags_li.append(tag.text)
#         data.append({"title": title, "description": description, "link": link, "tags": tags_li})

# Save to CSV and JSON
# df = pd.DataFrame(data)
# df.to_csv("mechanism_institute_library.csv", index=False)
# with open("mechanism_institute_library.json", "w") as f:
#     json.dump(data, f, indent=4)

# Check if the number of detected links matches the number of entries in JSON
# if len(links) == len(data):
#     print(f"Success: The number of scraped entries ({len(data)}) matches the number of detected cards.")
# else:
#     print(f"Warning: The number of scraped entries ({len(data)}) does not match the number of detected cards ({len(cards)}).")

#scrape all data
for item in data:
    driver.get(item['link'])

    #load page
    load_page()
    
    #initializing lists
    tags_li = []
    resources = []
    examples = []
    
    #scraping title, description
    content = driver.find_element(By.CLASS_NAME, "max-w-\\[720px\\]")
    title = content.find_element(By.XPATH, "//p[contains(@class, 'text-[48px]')]").text
    description = content.find_element(By.XPATH, "//p[contains(@class, 'text-[22px]')]").text

    #scraping tags
    tags = content.find_elements(By.XPATH, "//span[contains(@class, 'text-xs')]")
    for tag in tags:
        tags_li.append(tag.text)

    #scraping details
    try:
        info = content.find_element(By.TAG_NAME, "article")
        details = ''
        for child in info.find_elements(By.XPATH, "./*"):
            if child.tag_name == 'p':
                details = details + child.text + "\n"
            elif child.tag_name == 'ul':
                for li in child.find_elements(By.TAG_NAME, "li"):
                    details = details + li.text + "\n"
    except:
        details = "No details"

    #scraping resources content
    try:
        resource = content.find_element(By.XPATH, "//div[p[text()='Resources']]")
        for ul in resource.find_elements(By.TAG_NAME, "ul"):
            for li in ul.find_elements(By.TAG_NAME, "li"):
                resources_li = li.text
                a_tag = li.find_element(By.TAG_NAME, "a")
                resources_links_li = a_tag.get_attribute("href")
                resources.append({"resource": resources_li, "resources links":resources_links_li})
    except:
        resources.append({"resource": "", "resources links":""})

    #scraping examples content
    try:
        example = content.find_element(By.XPATH, "//div[p[text()='Examples']]")
        divs = example.find_elements(By.CLASS_NAME, "rounded-2xl")
        for div in divs:
            examples_links_li = []
            examples_details_li = []
            example_title = div.find_element(By.XPATH, ".//p[contains(@class, 'text-[20px]')]").text
            eg_links = div.find_elements(By.TAG_NAME, "a")
            for eg_link in eg_links:
                examples_links_li.append(eg_link.get_attribute("href"))
            eg_details = div.find_elements(By.CLASS_NAME, "text-\\[16px\\]")
            for det in eg_details:
                examples_details_li.append(det.text)
            examples.append({"example": example_title, "example_details": examples_details_li, "example_links": examples_links_li})
    except:
        examples.append({"example": "", "example_details": "", "example_links": ""})

    #initializing dictionary
    item_data = {
        "title": title,
        "description": description,
        "tags": tags_li,
        "details": details,
        "resources": resources,
        "examples": examples
    }

    data2.append(item_data)

#merging data lists
merged_data = []

for i in range(len(data)):
    # Create a new dictionary combining link info and other details
    merged_entry = {
        "link": data[i]["link"],
        **data2[i]  # Unpacking the dictionary from data2
    }
    merged_data.append(merged_entry)
    
#Save to CSV and JSON
df = pd.DataFrame(merged_data)
df.to_csv("mechanism_institute_library.csv", index=False)
with open("mechanism_institute_library.json", "w") as f:
    json.dump(merged_data, f, indent=4)

# Close the browser
driver.quit()
