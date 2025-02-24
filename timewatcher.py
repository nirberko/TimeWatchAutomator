import os
import json
import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
import re

CONFIG_PATH = 'config.json'

ABSENCE_CELL_NUMBER = 3
DAY_TYPE_NUMBER = 1
FULL_DATE_TYPE_NUMBER = 0
FREE_DAYS = [u'שישי', u'שבת', u'ערב חג', u'חג']

def extract_date(date_string):
    # Use regex to match the date pattern
    match = re.match(r'\d{2}-\d{2}-\d{4}', date_string)
    if match:
        return match.group(0)
    return None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_config(config_path):
    with open(config_path) as f:
        config = json.loads(f.read())
    return config


def login(driver):
    driver.get('https://checkin.timewatch.co.il/punch/punch.php')
    config = get_config(CONFIG_PATH)
    e = driver.find_element(By.ID, 'login-comp-input')
    e.send_keys(config['company_id'])
    e = driver.find_element(By.ID, 'login-name-input')
    e.send_keys(config['user_id'])
    e = driver.find_element(By.ID, 'login-pw-input')
    e.send_keys(config['password'])
    e = driver.find_element(By.CSS_SELECTOR, 'button[type=submit]')
    e.click()


def wait_for_document_ready(driver):
    while driver.execute_script('return document.readyState;') != 'complete':
        time.sleep(0.001)
    while len(driver.find_elements(By.ID, 'jqibox')) > 0:
        time.sleep(0.001)


def wait_for_modal_to_close(driver):
    while len(driver.find_elements(By.CLASS_NAME, 'modal')) > 0:
        time.sleep(0.001)


def click_on_confirm(driver, retries=0):
    if retries > 5:
        raise Exception('Failed to click on confirm button')
    try:
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, 'button.modal-popup-btn-confirm').click()
    except:
        click_on_confirm(driver, retries + 1)


def fill_timewatch(driver):
    config = get_config(CONFIG_PATH)
    entrance_hour_hour, entrance_hour_minute = config['entrance_hour'].split(':')
    leaving_hour_hour, leaving_hour_minute = config['leaving_hour'].split(':')

    fill_form_script = "$('input#ehh0').val('%s');$('input#emm0').val('%s');$('input#xhh0').val('%s');$('input#xmm0').val('%s');$('input[type=image]').click()"
    fill_form_script = fill_form_script % (
        entrance_hour_hour, entrance_hour_minute, leaving_hour_hour, leaving_hour_minute)

    table = driver.find_element(By.CLASS_NAME, 'table-responsive')
    rows = table.find_elements(By.CLASS_NAME, 'tr')

    has_day_name = True
    days_links_len = len(rows)
    # Missing "Shem Yom" (day name)
    if len(rows[0].find_elements(By.CSS_SELECTOR, 'td')) == 13:
        has_day_name = False

    for link_num in range(days_links_len):
        try:
            table = driver.find_element(By.CLASS_NAME, 'table-responsive')
            rows = table.find_elements(By.CLASS_NAME, 'tr')
            link = rows[link_num]

            date = link.find_elements(By.CSS_SELECTOR, 'td')[
                FULL_DATE_TYPE_NUMBER].text.strip()

            if has_day_name and u'יום מנוחה' in link.text:
                continue
            elif not has_day_name and link.find_elements(By.CSS_SELECTOR, 'td')[
                DAY_TYPE_NUMBER].text.strip() in FREE_DAYS:
                continue
            if link.find_elements(By.CSS_SELECTOR, 'td')[ABSENCE_CELL_NUMBER].text.strip():
                continue
            link.click()
            wait_for_document_ready(driver)
            driver.execute_script(fill_form_script)
            click_on_confirm(driver)
            wait_for_modal_to_close(driver)

            print(bcolors.OKGREEN + f"Filled day {extract_date(date)} successfully" + bcolors.ENDC)

        except StaleElementReferenceException:
            print(f"Encountered StaleElementReferenceException at row {link_num}, retrying...")
            continue

        time.sleep(config['time_threshold_sec'])


def select_month(driver, month: int):
    month_select = driver.find_element(By.CSS_SELECTOR, 'select.form-control[name=month]')
    month_select.find_elements(By.TAG_NAME, 'option')[month - 1].click()
    time.sleep(0.5)

def select_year(driver, year: int):
    year_select = driver.find_element(By.CSS_SELECTOR, 'select.form-control[name=year]')

    for option in year_select.find_elements(By.TAG_NAME, 'option'):
        if option.get_attribute('value') == str(year):
            option.click()
            break

    time.sleep(0.5)


def main(month, year):
    # Set up Chrome options for headless mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    

    login(driver)
    driver.find_element(By.PARTIAL_LINK_TEXT, 'עדכון נתוני נוכחות').click()

    select_month(driver, month)
    select_year(driver, year)
    fill_timewatch(driver)
    driver.close()


def generate_config():
    company_id = input("Please enter company id: ")
    user_id = input("Please enter user id: ")
    password = input("Please enter password (probably ID), notice will be stored plain-text: ")
    entrance_hour = input("Please enter your entrance hour. leave empty for default (09:00): ")

    if not entrance_hour:
        entrance_hour = '09:00'
    leaving_hour = input("Please enter your leaving hour. leave empty for default (18:00): ")
    if not leaving_hour:
        leaving_hour = '18:00'

    time_threshold_sec = input(
        "Please enter the time threshold (in seconds) for actions in seconds (default is 2 seconds): ")
    if not time_threshold_sec:
        time_threshold_sec = 2
    else:
        time_threshold_sec = int(time_threshold_sec)


    config = {'company_id': company_id, 'user_id': user_id, 'password': password, 'entrance_hour': entrance_hour,
              'leaving_hour': leaving_hour, 'time_threshold_sec': time_threshold_sec}
    with open(CONFIG_PATH, 'w') as f:
        f.write(json.dumps(config))

    return config


if __name__ == '__main__':
    if not os.path.exists(CONFIG_PATH):
        print('Config file "%s" does not exist. generating for next time...' % CONFIG_PATH)
        res = generate_config()
        month = res['month']
        
    current_month = time.localtime().tm_mon
    month_input = input(f"Please enter the month number (default is current month - {current_month}): ")
    month = int(month_input) if month_input else current_month

    current_year = time.localtime().tm_year
    year_input = input(f"Please enter the year number (default is current year - {current_year}): ")
    year = int(year_input) if year_input else current_year
        
    main(month, year)

    print(bcolors.OKGREEN + 'Done!' + bcolors.ENDC)