import os
import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open Website
driver.get("https://www.wedmegood.com/vendor-login")


# Get today's date for the folder name
current_date = datetime.now().strftime("%Y-%m-%d")
report_dir = os.path.join("report", current_date)

# Create the directory
os.makedirs(report_dir, exist_ok=True)

# unique file names - timestamp
timestamp = datetime.now().strftime("%H-%M-%S")  
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# file name formation
txt_filename = f"vendor_login_success_{timestamp}.txt"
csv_filename = f"vendor_login_success_{timestamp}.csv"

# Full file paths
txt_report_path = os.path.join(report_dir, txt_filename)
csv_report_path = os.path.join(report_dir, csv_filename)

# Report files
#txt_report = f"login_report_{timestamp}.txt"
#csv_report = f"login_report_{timestamp}.csv"


with open(txt_report_path, "w", encoding="utf-8") as txt, open(csv_report_path, "a", newline="", encoding="utf-8") as csv_file:

    csv_writer = csv.writer(csv_file)

    # CSV Header
    if csv_file.tell() == 0:
        csv_writer.writerow(["Timestamp", "Email", "Status", "URL", "Error"])

    try:
        txt.write("---- Login Test Report ----\n")
        txt.write(f"Test Start Time: {current_time}\n\n")

        email = "maygup@yahoo.com"
        password = "123456"
        

        # Enter Email
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='email-phone-field']"))
        ).send_keys(email)

        # Click Continue
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='log-in']"))
        ).click()

        # Enter Password
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter password']"))
        ).send_keys(password)

        # Click Submit
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        ).click()

        # Verify Login Success
        WebDriverWait(driver, 10).until(EC.url_contains("vendor-dashboard"))

        success_message = f"{current_time} | Login successful! URL: {driver.current_url}\n"
        print(success_message)
        txt.write(success_message)
        csv_writer.writerow([current_time, email, "Success", driver.current_url, ""])

    except Exception as e:
        error_message = f"{current_time} | Login failed! Error: {str(e)}\n"
        print(error_message)
        txt.write(error_message)
        csv_writer.writerow([current_time, email, "Failed", "", str(e)])

    finally:
        # Closing Browser
        driver.quit()
        txt.write("\n---- End of Report ----\n")

print(f" TXT Report saved: {txt_filename}")
print(f" CSV Report saved: {csv_filename}")
