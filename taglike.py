from msedge.selenium_tools import Edge, EdgeOptions
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from getpass import getpass


def get_username(card):
    username = card.find_element_by_xpath(
        './/span[contains(text(),"@")]').text
    return username


def login(my_password):
    sleep(2)
    username = driver.find_element_by_xpath(
        '//input[@autocomplete="username"]')
    username.send_keys('roasteanne')
    username.send_keys(Keys.RETURN)
    sleep(2)
    password = driver.find_element_by_xpath(
        '//input[@autocomplete="current-password"]')
    password.send_keys(my_password)
    password.send_keys(Keys.RETURN)


# get input
password = getpass("Password: ")
link_input = input("Masukin link gan: ")

# create instance of web driver
options = EdgeOptions()
options.use_chromium = True
driver = Edge(options=options)

# navigate to the login page
driver.get('https://www.twitter.com/login')
driver.maximize_window()

# check if we already logged in
current_url = driver.current_url

if(current_url != "https://twitter.com/home"):
    # do login procedure
    login(password)

# navigate to the link
sleep(5)
url = link_input + '/likes'
driver.get(url)
driver.maximize_window()

unames = []

# scrolling
sleep(2)
pop_up_window = driver.find_element_by_xpath(
    '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div')
last_position = driver.execute_script("return arguments[0].scrollHeight;",
                                      pop_up_window)
scrolling = True

while scrolling:
    page_cards = driver.find_elements_by_xpath(
        '//div[@aria-label="Timeline: Liked by"]//div[@data-testid="UserCell"]')
    for card in page_cards:
        uname = get_username(card)
        if uname and uname not in unames:
            unames.append(uname)

    scroll_attempt = 0
    while True:
        # check scroll position
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);",
                              pop_up_window)
        sleep(1)
        curr_position = driver.execute_script("return arguments[0].scrollHeight;",
                                              pop_up_window)

        if last_position == curr_position:
            scroll_attempt += 1

            # end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2)
        else:
            last_position = curr_position
            break

# print semuanya
print("\n------------ HASIL ------------")
print("Jumlah likes: ", len(unames))
if("@OOTDFESS" in unames):
    unames.remove("@OOTDFESS")
for u in unames:
    print(u+" ", end='')

driver.quit()
