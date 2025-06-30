from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time

# Constants
LOGIN_URL = "http://web:80/"
COMMENT_URL = "http://web:80/comment"
USERNAME = "3y_adm!n!strat0r"
PASSWORD = "sup3rs3cur3p@ssw0rd"
WAIT_TIME = 60  # seconds

# Headless Firefox setup
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(options=options)

try:
    print("[*] Visiting login page...")
    driver.get(LOGIN_URL)

    print("[*] Waiting for login fields...")
    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    # Fill in credentials
    driver.find_element(By.NAME, "username").send_keys(USERNAME)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    print("[+] Submitted login form.")

    # Wait for login result
    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    if "Access Granted" in driver.page_source:
        print("[✅] Admin login successful.")
        time.sleep(WAIT_TIME)

        driver.get(COMMENT_URL)

        print("[*] Waiting for comment form...")
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.NAME, "author"))
        )

        AUTHOR = "3y_adm!n!strat0r"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        MESSAGE = f"Admin was here at {now}"

        driver.find_element(By.NAME, "author").send_keys(AUTHOR)
        driver.find_element(By.NAME, "message").send_keys(MESSAGE)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        print(f"[+] Commented: {MESSAGE}")

    else:
        print("Login may have failed.")

except TimeoutException:
    print("[!] Timeout: Could not find elements within 120 seconds.")

finally:
    driver.quit()
