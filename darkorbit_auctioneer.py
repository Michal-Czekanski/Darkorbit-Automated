# darkorbitBot.py
password = '#my_password'

#//////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pywinauto, time
from time import sleep
import sys


url = 'http://darkorbit.pl'
username = '#my_nickname'





# Launch browser
def browser():
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','true')
    firefox_profile.set_preference('plugin.state.flash',2)
    browser = webdriver.Firefox(firefox_profile)
    browser.get(url)
    return browser

# Login
def key_sender(elem, keys):
    elem.send_keys(keys)

def login(driver):
    login_css = "[id*='login_form_username']"
    login_elem = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, login_css)) )

    key_sender(login_elem, username)

    password_css = "[id*=login_form_password]"
    password_elem = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, password_css)) )

    key_sender(password_elem, password)
    key_sender(password_elem, Keys.ENTER)

# Close popup ads by refreshing browser

def close_ads(driver):
    ads_css = "[id*='button_close']"
    ads_elem = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ads_css)) )
    if ads_elem:
        driver.refresh()

def ok_clicker(driver):
    ok_css = ".ok_button"
    ok_elem = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ok_css)) )
    driver.refresh()

       
def auction_open(driver):
    auction_css = "#trade_btn"
    auction_elem = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, auction_css)) )
    auction_elem.click()

def auction_items_finder(driver):
    auction_item_css = 'td[class="auction_item_name_col"]'
    auction_items_list = WebDriverWait(driver, 20).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, auction_item_css)) )
    return auction_items_list


def auction_items_prices_finder(driver):
    auction_item_price_css = 'td[class="auction_item_current"]'
    auction_items_prices_list = WebDriverWait(driver, 20).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, auction_item_price_css)) )
    prices_list = [(int(''.join(item_price.text.split('.')))) for item_price in auction_items_prices_list]
    return prices_list

def check_who_owns(driver):
    owner_css = "td.auction_item_highest"
    owner_elems = WebDriverWait(driver, 20).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, owner_css)) )
    owners_list = [owner.text for owner in owner_elems]
    return owners_list

def auction_box_scroller(driver, key=Keys.PAGE_DOWN):
    auction_box_css = ".auction_item_wrapper.jspScrollable"
    auction_box_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, auction_box_css)) )
    auction_box_element.send_keys(key)



def do_bid(driver, clickable_item, scroll_range, old_items_list, old_items_prices_list):

    element_clickable = False
    try:
        clickable_item.click()
        element_clickable = True
    except Exception as e:
        print(e)
        print('CANNOT CLICK ON {}, SCROLLING UP AND DOWN'.format(clickable_item.text))
        
        for i in range(2):
            auction_box_scroller(driver)
        for i in range(2):
            auction_box_scroller(driver, key=Keys.PAGE_UP)
        
        try: 
            clickable_item.click()
            element_clickable = True
        except Exception as e2:
            print(e2)
            print("CLICK IS NOT POSSIBLE, KEEP GOING")

    # If element was clicked
    if element_clickable:    
        bid_css = "#auction_place_bid"
        bid_elem = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, bid_css)) )
        bid_elem.click()
        
        notification_css = "div[onclick*='closeInfoLayer'].popup_shop_close_text"
        notification_elem = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.CSS_SELECTOR, notification_css)) )
        notification_elem.click()


        for x in range(scroll_range):
            auction_box_scroller(driver, key=Keys.PAGE_DOWN)

        # make a new list of items prices
        
        new_items_list = auction_items_finder(driver)
        new_items_prices_list = auction_items_prices_finder(driver)

        return new_items_list, new_items_prices_list

    # If element couldn't be clicked
    else:
        return old_items_list, old_items_prices_list








#
# MAIN FUNCTION COORDINATING WHOLE AUCTION PROCESS
#
           
def auction_process(driver):
    
    
    
    for scroll in range(8):
        if scroll > 0:
            auction_box_scroller(driver)
        already_checked = []


        items_list = auction_items_finder(driver)
        items_prices_list = auction_items_prices_finder(driver)
        current_owners = check_who_owns(driver)
        
        
        for i in range(6):

            item = items_list[i]
            item_price = items_prices_list[i]
            owner = current_owners[i]

            if owner == '#my_username':
                already_checked.append(item)
            
            if not(item in already_checked):
                
                print(item.text + ": " + str(item_price) + ' - ' + owner)
                if item.text == "Iris":
                    if item_price <= 20000000:
                        items_list, items_prices_list = do_bid(driver, item, scroll, items_list, items_prices_list)
                elif item.text == "Napęd G3N-7900" or item.text == "Osłona SG3N-B02":
                    if item_price <= 2000000:
                        items_list, items_prices_list = do_bid(driver, item, scroll, items_list, items_prices_list)
                               
                elif item_price <= 20000:
                    items_list, items_prices_list = do_bid(driver, item, scroll, items_list, items_prices_list)
                    

                                   
                else:
                    already_checked.append(item)
                

        

     

driver = browser()
login(driver)
close_ads(driver)




i = 0

while True:

    start = time.time()

    auction_open(driver)
    auction_process(driver)

    end = time.time()
    elapsed = end - start

    i += 1
    print("\n\nROUND {}\nDONE IN {} MINUTES\n\n".format(i,elapsed/60))

