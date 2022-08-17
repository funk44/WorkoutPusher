from winreg import HKEY_CURRENT_USER, OpenKey, QueryValueEx

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import os


def get_driver(browser):
    """ Function to check driver version matches the installed 
        browser version and set the webdriver to headless """
    try:
        if browser == 'Firefox':
            options = FireFoxOptions()
            options.headless = True
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        elif browser == 'Edge':
            options = EdgeOptions()
            options.add_argument('headless')
            options.add_argument('disable-gpu')
            driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install(), options=options)
        else:
            options = ChromeOptions()
            #options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

        return driver
    except:
        return 'No driver'


def default_brower_windows():
    """ Function to check registery to dermine default driver version
        and version installed  """
    try:
        if os.system() == 'Windows':
            with OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as regkey:
                browser_choice = QueryValueEx(regkey, 'ProgId')[0]
                if 'edge' in browser_choice.lower():
                    browser = 'Edge'
                elif 'chrome' in browser_choice.lower():
                    browser = 'Chrome'
                elif 'firefox' in browser_choice.lower():
                    browser = 'Firefox'

        return browser
    except:
        return 
