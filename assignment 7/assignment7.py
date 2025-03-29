import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu") 
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://dressx.com/news/ai-avatar-customization-helps-businesses-stay-ahead-in-virtual-ecosystems"
driver.get(url)
element = driver.find_element(By.CSS_SELECTOR, 'p') # getting just the 1st paragraph
img_elements_links = [elem.get_attribute('src') for elem in driver.find_elements(By.CSS_SELECTOR, 'img')] # getting the link to every image that comes up on that URL.
print(element.text) # prints empty text, so there are many p elements before the p element holding the first paragraph of article. no problem as we only want the images.
for i in range(len(img_elements_links)):
    img_data = requests.get(img_elements_links[i]).content
    with open(f'imgs/image_{i}.jpg', 'wb') as handler:
        handler.write(img_data)
driver.quit()
