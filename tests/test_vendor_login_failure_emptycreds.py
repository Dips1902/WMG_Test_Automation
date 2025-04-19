import os
import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get today's date for the folder name
current_date = datetime.now().strftime("%Y-%m-%d")
report_dir = os.path.join("report", current_date)

# Create the directory if it doesn't exist
os.makedirs(report_dir, exist_ok=True)

# Generate timestamp for unique file names
timestamp = datetime.now().strftime("%H-%M-%S")  
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Define report file names
txt_filename = f"vendor_login_failure_emptycreds_{timestamp}.txt"
csv_filename = f"vendor_login_failure_emptycreds_{timestamp}.csv"

# Full file paths
txt_report_path = os.path.join(report_dir, txt_filename)
csv_report_path = os.path.join(report_dir, csv_filename)

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get("https://www.wedmegood.com/vendor-login")

# Wait for the email field & enter an incorrect email
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@id='email-phone-field']"))
).send_keys("")

# Click Continue button to proceed
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@id='log-in']"))
).click()

# Wait for a few seconds for the error message to appear
time.sleep(3)

# Check for the error message
try:
    error_message = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Email or Phone is Mandatory')]"))
    )
    test_result = "Test Passed: Login failed as expected."
except:
    test_result = "Test Failed: Incorrect credentials logged in!"

# Save the test result to reports
with open(txt_report_path, "w", encoding="utf-8") as report_file:
    report_file.write(test_result)

# Append results to CSV
csv_exists = os.path.exists(csv_report_path)
with open(csv_report_path, "a", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    if not csv_exists:
        csv_writer.writerow(["Timestamp", "Status"])
    csv_writer.writerow([current_time, test_result])

# Print the result to the console
print(test_result)

# Close the browser
driver.quit()
