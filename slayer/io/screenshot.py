"""
The goal of this module is to ease the creation of static maps
from this package.

Ideally, this is done headlessly (i.e., no running browser)
and quickly. Given that deck.gl requires WebGL, there aren't
lot of alternatives to using a browser.

Not yet implemented.
"""
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# TODO this should be determined programmatically
CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
WINDOW_SIZE = "1920,1080"


def make_screenshot(url, output):
    # options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH
    )
    driver.get(url)
    driver.save_screenshot(output)
    driver.close()

# This may be of interest
# https://github.com/stackgl/headless-gl


raise NotImplementedError(
    'This part of the library is not complete')
