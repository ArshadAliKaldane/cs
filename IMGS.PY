# import webdriver from selenium
from selenium import webdriver
# import By locator
from selenium.webdriver.common.by import By
import time
from threading import Thread

# set the browser to run in background
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--ignore-certificate-error")
options.add_argument("--incognito")


# create an instance of a browser (Chrome)
driver = webdriver.Chrome('./chromedriver', options=options)
# wait for the browser to load
driver.implicitly_wait(5)

# goto following url
url = 'https://goodreads.com'
# https://www.goodreads.com/#sitesearch_field
print('\nConnecting to',url,'\n')

img_urls = []
book_links = []
def main():
    driver.get(url)

    # get the title of the web-page
    print('\n',driver.title,'\n')

    with open("isbn.txt", "r") as f:
        isbn = [x.strip() for x in f]
    f.close()

    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div/div[2]/form/div/input").send_keys(isbn[0])
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div/div[2]/form/a/img").click()
    time.sleep(2)
    img_path = "/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[1]/div[1]/div[1]/a/img"
    img_urls.append(driver.find_element_by_xpath(img_path).get_attribute('src'))
    print(img_urls[-1])
    book_links.append(driver.current_url)
    print(book_links[-1])
    for x,n in enumerate(isbn):
        # search
        driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/header/div[1]/div/div[2]/form/input[1]").send_keys(isbn[x+1])
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/header/div[1]/div/div[2]/form/button").click()
        time.sleep(2)
        # get img_url
        img_urls.append(driver.find_element_by_xpath(img_path).get_attribute('src'))
        print(img_urls[-1])
        # get book_link
        book_links.append(driver.current_url)
        print(book_links[-1])

    # close the browser
    time.sleep(1)
    driver.quit()

if __name__ == "__main__":
    thread = Thread(target=main)
    thread.start()
    # save all images in a file
    with open("imgs.txt","a") as f:
        for url in img_urls:
            f.write(url)
    f.close()

    # save all links in a file
    with open("links.txt","a") as f:
        for url in book_links:
            f.write(url)
    f.close()

    print('done')