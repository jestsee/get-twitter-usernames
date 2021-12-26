from msedge.selenium_tools import Edge, EdgeOptions
from time import sleep
from selenium.common.exceptions import NoSuchElementException

url = input("Masukin URL nya gan: ")


def get_username(card):
    username = card.find_element_by_xpath(
        './/span[contains(text(),"@")]').text
    return username


def click_show():
    try:
        show = driver.find_element_by_xpath(
            '//span[contains(text(),"Show additional replies")]/parent::div/parent::div/parent::div/div[2]')
        if(show):
            show.click()
    except NoSuchElementException:
        return


# create instance of web driver
options = EdgeOptions()
options.use_chromium = True
driver = Edge(options=options)

# navigate to the link
driver.get(url)
driver.maximize_window()

unames = []
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    sleep(2)
    page_cards = driver.find_elements_by_xpath(
        '//article[@data-testid="tweet"]')
    for card in page_cards:
        uname = get_username(card)
        if uname and uname not in unames:
            unames.append(uname)

    scroll_attempt = 0
    while True:
        # check scroll position
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')
        sleep(1)
        curr_position = driver.execute_script("return window.pageYOffset;")

        if last_position == curr_position:
            scroll_attempt += 1

            # end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(3)
        else:
            last_position = curr_position
            break

# udah selesai scrolling, cek hidden rep
click_show()
sleep(3)
final_cards = driver.find_elements_by_xpath(
    '//article[@data-testid="tweet"]')
for card in final_cards:
    uname = get_username(card)
    if uname and uname not in unames:
        print(uname)
        unames.append(uname)

# print semuanya
print("\n------------ HASIL ------------")
print("Jumlah rep: ", len(unames)-1)
if("@OOTDFESS" in unames):
    unames.remove("@OOTDFESS")
for u in unames:
    print(u+" ", end='')

tes = input('udah semua bisa lanjut proses ga ya?')
while tes != 'y':
    tes = input('weh')

driver.quit()
# ? perlu nanganin kasus show more replies ga ya?
# TODO how scroll pop up windows (buat tag yg like nanti)
