from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from time import sleep

import database_functions


def icu_login(driver, username, password):
    """ Login to intervals.icu """
    driver.get('https://intervals.icu/login')

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//*[@name='email']"))).send_keys(username)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//*[@name='password']"))).send_keys(password)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='v-btn__content' and text()='Login']"))).click()
    
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//*[@class='red--text']")))
        return 
    except:
        return driver


def get_workout(driver):
    """ Check i.icu to determine if there is a workout 
    planned for the current date. Function also checks
    to see if the same workout has already been loaded 
    from a past run """
    
    #bypass the sign-up prompt NOTE: !!! PLEASE CONSIDER SUPPORTING !!!
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='v-icon material-icons theme--dark' and text()='close']"))).click()

    try: 
        #find todays workout and get the TrainerDay link
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='day day clickable today']//*[@title='Ride']"))).click()

        td_link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.markdown a"))).get_attribute('href')
        if td_link:
            if not 'trainerday' in td_link:
                return False, 'No workout found...'
            elif not database_functions.check_workout(td_link):
                database_functions.load_workout(td_link)
                return td_link, 'Workout found...'
            else:
                return False, 'Workout already added...'
        else:
            return False, 'No workout found...'
    except NoSuchElementException:
        return False, 'No workout found...'


def td_login(driver, username, password):
    """ Log into TrainerDay """
    driver.get('https://trainerday.com/login')

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wpforms-field-large wpforms-field-required']"))).send_keys(username)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(password)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wpforms-submit' and text()='Login']"))).click()

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wpforms-error-container']")))
        return 
    except:
        return driver


def push_workout(driver, td_link):
    """ Push the workout to TrainingPeaks """
    driver.get(td_link)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Send To')]"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'TrainingPeaks (Power)')]"))).click()

    #sleep to confirm send
    sleep(3)

    #kill the selenium instance now that its no longer needed
    driver.quit()