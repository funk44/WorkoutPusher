from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from datetime import datetime
from time import sleep
from pathlib import Path

import sqlite3
import os

#script path
MAIN_PATH = os.getcwd()

#USERNAME AND PASSWORDS
I_UNAME = ''
I_PW = ''

TD_UNAME = ''
TD_PW = ''

#time to sleep between checks
SLEEP_TIME = 60 * 30


def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    return driver


def startup():
    #checks if db exists and creates if none found
    sql_db = Path(MAIN_PATH + r'\workout.db')
    if not sql_db.is_file():
        conn = sqlite3.connect(sql_db)
        cur = conn.cursor()
        with conn:
            cur.execute('CREATE TABLE past_workouts (link TEXT PRIMARY KEY, load_date TEXT)')

        conn.close

    return sql_db


def get_workout(driver, sql_db):
    #navigate to main icu page
    driver.get('https://intervals.icu/')

    #login to intervals.icu
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='v-btn' and text()='Login']"))).click()

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//*[@name='email']"))).send_keys(I_UNAME)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f"//*[@name='password']"))).send_keys(I_PW)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='v-btn__content' and text()='Login']"))).click()

    #bypass the sign-up prompt NOTE: !!! STRONGLY CONSIDER SIGNING UP !!!
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='v-icon material-icons theme--dark' and text()='close']"))).click()

    #find todays workout and get the TrainerDay link
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='day day clickable today']//*[@class='activity']"))).click()
    td_link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.markdown a"))).get_attribute('href')

    if not check_workout(td_link, sql_db):
        return td_link
    else:
        driver.quit()
        return False


def push_workout(driver, td_link):
    #navigate to td login page
    driver.get('https://trainerday.com/login')

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wpforms-field-large wpforms-field-required']"))).send_keys(TD_UNAME)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(TD_PW)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='wpforms-submit' and text()='Login']"))).click()

    #now that we are logged in navigate to the workout page
    driver.get(td_link)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Send To')]"))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'TrainingPeaks (Power)')]"))).click()

    #sleep to confirm send
    sleep(5)

    driver.quit()


def check_workout(td_link, sql_db):
    #checks if workout has been found and sent to TD before
    conn = sqlite3.connect(sql_db)
    cur = conn.cursor()

    workout = cur.execute("SELECT 1 FROM past_workouts WHERE link=?", (td_link,)).fetchone()

    try:
        if workout:
            return True
        else:
            with conn:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cur.execute("INSERT INTO past_workouts VALUES(?,?)", (td_link, now))
            return False
    finally:
        conn.close()


if __name__ == '__main__':
    sql_db = startup()
    while True:
        driver = get_driver()
        td_link = get_workout(driver, sql_db)
        if td_link:
            push_workout(driver, td_link)

        sleep(SLEEP_TIME)