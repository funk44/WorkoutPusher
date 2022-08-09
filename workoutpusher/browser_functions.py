from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, OpenKey, QueryValueEx

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

import subprocess
import webbrowser


def get_driver(path, browser, settings, version):
    """ Function to check driver version matches the installed 
        browser version and set the webdriver to headless """
    executable = settings['Executables'][browser]
    driver_path = str(path) + '\\' + executable

    #NOTE: assumption is that firefox version is always up to date
    if check_driver_version(executable, version) and browser != 'Firefox':
        return 'Wrong version'

    try:
        if browser == 'Firefox':
            options = FireFoxOptions()
            options.headless = True
            driver = webdriver.Firefox(executable_path=driver_path, firefox_options=options)
        elif browser == 'Edge':
            options = EdgeOptions()
            options.add_argument('headless')
            options.add_argument('disable-gpu')
            driver = webdriver.Edge(executable_path=driver_path, options=options)
        else:
            options = ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(executable_path=driver_path, options=options)

        return driver
    except:
        return 'No driver'


def check_driver_version(executable, version):
    "Function to check if correct webdriver version is installed"
    driver_version = subprocess.Popen(f'{executable} -v', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
    driver_version = driver_version.split(' ')[1][:2]
    
    browser_version = version[:6]

    if driver_version != browser_version:
        return True


def default_brower_windows():
    """ Function to check registery to dermine default driver version
        and version installed  """
    try:
        with OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as regkey:
            browser_choice = QueryValueEx(regkey, 'ProgId')[0]

        with OpenKey(HKEY_CLASSES_ROOT, r'{}\shell\open\command'.format(browser_choice)) as regkey:
            browser_path_tuple = QueryValueEx(regkey, None)

            browser_path = browser_path_tuple[0].split('"')[1]
            browser_path = str(browser_path).replace('\\', '\\\\')

            if 'edge' in browser_path.lower():
                browser = 'Edge'
            elif 'chrome' in browser_path.lower():
                browser = 'Chrome'
            elif 'firefox' in browser_path.lower():
                browser = 'Firefox'

            if browser == 'Firefox':
                version = subprocess.Popen(f'"{browser_path}" -v|more', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
                version = (version.rsplit(' ')[2])[:2]
            else:
                version = subprocess.Popen(f'wmic datafile where name="{browser_path}" get Version /value', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()[0].decode('utf-8').strip()
                version = (version.rsplit('=')[1])

        return browser, version
    except:
        return 


def download_driver(settings, browser, version):
    """ If not driver is not found or version is incorrect 
        prompt user to download """

    top = settings['Tops'][browser]
    dl = settings['Tails'][browser]
    
    if browser != 'Firefox':
        link = top + str(version) + '/' + dl
    else:
        link = top + dl

    webbrowser.open_new_tab(link)
