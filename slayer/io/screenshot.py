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
