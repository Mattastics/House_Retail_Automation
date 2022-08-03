import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time, requests, lxml

google_form = "https://docs.google.com/forms/d/e/1FAIpQLSdxU9YkCpP9L4D_iYMq4y0o0ZtN8VbLwgxND4AOMkyV0m3C-Q/viewform" \
              "?usp=sf_link"
zillow_link = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
    "Accept-Language": "en-US"
}

response = requests.get(url=zillow_link, headers=headers)
response.raise_for_status()
zillow_page = response.text
soup = BeautifulSoup(zillow_page, "lxml")

links = [links.get("href") for links in soup.findAll(name="a", class_="list-card-link", tabindex="0")]
for i in range(len(links)):
    if not links[i].startswith("http"):
        links[i] = "https://wwww.zillow.com" + links[i]

prices = []
prices_list = soup.findAll(class_="list-card-price")
for p in prices_list:
    if '+' in p.text:
        prices.append(p.getText().split('+')[0])
    elif '/' in p:
        prices.append(p.getText().split('/')[0])
    elif ' ' in p:
        prices.append(p.getText().split(' ')[0])
    else:
        prices.append(p.getText())

addresses = []
addresses_list = soup.findAll(class_="list-card-addr")
for a in addresses_list:
    addresses.append(a.getText())

CHROME_DRIVER = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=CHROME_DRIVER)

time.sleep(5)

for n in range(len(links)):
    driver.get(google_form)

    time.sleep(2)
    address = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

    address.send_keys(addresses[n])
    price.send_keys(prices[n])
    link.send_keys(links[n])
    submit_button.click()
