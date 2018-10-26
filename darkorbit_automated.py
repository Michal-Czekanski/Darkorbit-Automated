# darkorbit_automated.py
password = '#my_password'


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pywinauto, time
from time import sleep


url = 'http://darkorbit.pl'
username = '#my_username'

# Before launching browser enable Adobe Flash Player

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','true')
firefox_profile.set_preference('plugin.state.flash',2)


# A piece of code to check last time that bot has been used, if it's 6 hours, launch bot.


# darkTimer.py

def d_timer(file_path):
    file = open(file_path)

    last_execution, time_left = [float(x) for x in file.readlines()]
    now = time.mktime(time.localtime())

    difference = now - last_execution

    if difference < 21600:
        return time_left
    else:
        return 0
    

def sleep_count(sleep_time, save_time = False):
    print('sleeping {} seconds'.format(sleep_time))
    for i in range(1, int(sleep_time) + 1):
        print(i)

        # Update time in a file
        # if this function is used to measure time between resources transporting
        if save_time == True:
                if i in range(60, 21600, 60):
                    file = open(r'.\darkorbitBot_time.txt')
                    last_launch, time_left = file.read().split('\n')
                    file.close()

                    updated_time = float(time_left) - 60
                    file = open(r'.\darkorbitBot_time.txt', 'w')
                    file.write(last_launch + '\n' + str(updated_time))
                    file.close()
                        
        sleep(1)


# Launch browser
def browser():
    browser = webdriver.Firefox(firefox_profile)
    browser.get(url)
    sleep(3)
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
    
# Click Skylab

def ok_clicker(driver):
    ok_css = ".ok_button"
    ok_elem = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ok_css)) )
    driver.refresh()

def promerium_receive(driver):
    skylab_css = "[id*='lab']"
    skylab_elem = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, skylab_css)) )
    skylab_elem.click()
    # If there's [ok button] click it
    try:
        ok_clicker(driver)
    except:
        pass
    

# Click Start button

def game_launcher(driver):
    launch_css = "#header_start_btn"
    launch_elem = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, launch_css)) )
    launch_elem.click()



def interact_with_game_start(tuple_coords, sleep_time=60):

    # Wait for the window to appear
    sleep(10)
    
    # Click Start in game window
    app = pywinauto.application.Application()
    darkorbit_windows = app.connect(title_re="Darkorbit -")
    game_window = darkorbit_windows.window(title_re ='Darkorbit - Mozilla Firefox')
    game_hwnd = game_window.wrapper_object()

    game_hwnd.maximize()
    game_hwnd.minimize()
    
    sleep_count(sleep_time)

    # DEBUG
    print('Clicking start')
    # DEBUG
    
    game_hwnd.click_input(coords = tuple_coords)
    sleep(1)
    game_hwnd.minimize()
    return game_hwnd

def interact_with_game_sell(hwnd, tuple_coords, sleep_time=30):
    sleep_count(sleep_time)

    print("Clicking trade button")
    hwnd.click_input(coords=tuple_coords)
    
    print("Selling promerium")
    sleep(2)
    promerium_coords = (846, 466)
    hwnd.click_input(coords=promerium_coords)
    sleep(1)
    print("Promerium sold.")
    hwnd.close_alt_f4()



def interact_with_game():

    game = interact_with_game_start((690, 715), sleep_time=120)

    interact_with_game_sell(game, (790, 405), sleep_time=120)


        
# Send resources

def promerium_send(amount, driver):
    driver.refresh()
    sleep(30)
    driver.refresh()
    sleep(5)
    
    transport_css = "[onclick*=\"('transport\"]"
    transport_elem = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, transport_css)) )
    transport_elem.click()

    promerium_css= "#count_promerium"
    try:
        promerium_elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, promerium_css)) )
        promerium_elem.send_keys(amount)

        send_css = "[href*=\"sendTransport('normal')\"]"
        send_elem = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR, send_css)) )
        send_elem.click()
        
        ok_clicker(driver)
        
    except:
        pass
    
    finally:
        driver.quit()


   
def bot():

    tm_left = d_timer(r'.\darkorbitBot_time.txt')
    
    if tm_left > 0:
        sleep_count(tm_left, save_time = True)

     
    driver = browser()

    login(driver)
    
    close_ads(driver)

    promerium_receive(driver)

    game_launcher(driver)
    
    interact_with_game()
    
    promerium_send('3000', driver)
    
    with open('darkorbitBot_time.txt', 'w') as f:
        f.write(str(time.mktime(time.localtime())) + '\n21600' )
        f.close()


while True:    
    bot()






