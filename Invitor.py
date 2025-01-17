import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# Load mobile numbers from the Excel file
def load_mobile_numbers(file_path, column_name="CONTACT NO."):
    """Load mobile numbers from the Excel file."""
    try:
        df = pd.read_excel(file_path)
        return df[column_name].dropna().astype(str).tolist()
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []


# Get WhatsApp group members
def get_whatsapp_group_members(driver, group_name):
    """Retrieve the list of current WhatsApp group members."""
    try:
        # Search for the group
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.clear()
        search_box.send_keys(group_name)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)

        # Open group info
        group_header = driver.find_element(By.XPATH, '//header[@class="_24-Ff"]')
        group_header.click()
        time.sleep(2)

        # Scrape group members
        members = []
        members_list = driver.find_elements(By.XPATH, '//div[@role="button"]//span[@dir="auto"]')
        for member in members_list:
            members.append(member.text)

        print(f"Group members fetched: {len(members)}")
        return members
    except Exception as e:
        print(f"Error fetching group members: {e}")
        return []


# Send WhatsApp message with the group invite link to the missing members
def send_whatsapp_message(driver, phone_number, group_link):
    """Send a WhatsApp message with the group invite link to a given phone number."""
    try:
        # Custom message to send
        message = f"YOUR MESSAGE . \n \n{group_link}"

        # Construct the WhatsApp link
        whatsapp_link = f"https://wa.me/{phone_number}?text={message}"
        driver.get(whatsapp_link)

        # Wait for the page to load fully
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Continue to chat')]")))

        # Click the "Continue to chat" button if it appears
        try:
            continue_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Continue to chat')]")
            continue_button.click()
            print(f"Clicked 'Continue to Chat' for {phone_number}")
        except:
            print(f"No 'Continue to Chat' button found for {phone_number}. Proceeding...")

        # Wait for the message box to be available
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]')))
        message_box.send_keys(message)
        message_box.send_keys(Keys.RETURN)  # Send the message
        print(f"Invite link sent to {phone_number}")

        # Wait for the message to be sent (check if the sent message appears)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "{group_link}")]')))
        print(f"Message successfully sent to {phone_number}.")

    except Exception as e:
        print(f"Error sending invite to {phone_number}: {e}")


if __name__ == "__main__":
    # Constants
    EXCEL_PATH = r"PATH_TO_YOUR_EXCEL_FILE"  # Update with your file path
    GROUP_NAME = "GROUP_NAME"  # The WhatsApp group name
    MOBILE_COLUMN = "CONTACT NO."  # The column name containing mobile numbers in the Excel file
    GROUP_INVITE_LINK = "INSERT_YOUR_GROUP_LINK_HERE"  # The WhatsApp group invite link

    # Step 1: Load mobile numbers from Excel
    excel_numbers = load_mobile_numbers(EXCEL_PATH, MOBILE_COLUMN)
    if not excel_numbers:
        print("No numbers loaded from Excel. Check the file path or column name.")
        exit()

    # Step 2: Open WhatsApp Web using Selenium
    service = Service(r"PATH_TO_CHROMEDRIVER")  # Update with the path to your ChromeDriver
    options = Options()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com")
    input("Scan the QR code on WhatsApp Web and press Enter...")

    # Step 3: Get WhatsApp group members
    group_members = get_whatsapp_group_members(driver, GROUP_NAME)
    group_members_set = set(group_members)

    # Step 4: Find missing numbers
    missing_numbers = [num for num in excel_numbers if num not in group_members_set]
    print(f"Missing numbers: {missing_numbers}")

    # Step 5: Send WhatsApp invite links to the missing members
    if missing_numbers:
        for number in missing_numbers:
            send_whatsapp_message(driver, number, GROUP_INVITE_LINK)
    else:
        print("No missing numbers to send invites.")

    # Step 6: Close the browser
    driver.quit()
