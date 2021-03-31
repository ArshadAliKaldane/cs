# import webdriver from selenium
from selenium import webdriver
# import By locator
from selenium.webdriver.common.by import By
import time

# set the browser to run in background
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--ignore-certificate-error")
#options.add_argument("--incognito")


# create an instance of a browser (Chrome)
driver = webdriver.Chrome('./chromedriver', options=options)
# wait for the browser to load
driver.implicitly_wait(5)


# goto following url
url = 'https://goodreads.com'
# https://www.goodreads.com/#sitesearch_field
print('\nConnecting to',url,'\n')
driver.get(url)

# get the title of the web-page
print('\n',driver.title,'\n')
'''
# TODO:
credentials = {
    "email":"arshadalikaldane0987@gmail.com",
    "password":"gr@AK0165"
}

# signin /html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div/div[2]/form/div/input
driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[1]/div/div/form/div[1]/input[1]").send_keys(credentials['email'])
driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[1]/div/div/form/div[2]/div/input").send_keys(credentials['password'])
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[1]/div/div/form/div[3]/input[1]").click()

time.sleep(3)
# search for book
driver.find_element_by_xpath("/html/body/div[2]/div/header/div[1]/div/div[2]/form/input[1]").send_keys("0062310712")
time.sleep(3)
driver.find_element_by_xpath("/html/body/div[2]/div/header/div[1]/div/div[2]/form/button").click()

# get image
time.sleep(3)
img_url = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/a/img").get_attribute('src')
print('\n',img_url,'\n')

#get description /html/body/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div/span[1]
desc1 = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/span[1]").text
desc2 = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/span[2]").text
print('\n',desc1+desc2,'\n')
'''

driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div/div[2]/form/div/input").send_keys()
# close the browser
time.sleep(1)
driver.quit()
print('done')