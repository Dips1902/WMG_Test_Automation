import os
import csv
import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import paramiko
import pymysql
import pandas as pd
from sshtunnel import SSHTunnelForwarder
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# SSH details
ssh_host = "35.244.10.17"
ssh_port = 22
ssh_user = "deepti"
ssh_private_key = "C:\\Users\\deept\\.ssh\\id_rsa_no_pass"
ssh_passphrase = None

# Database details
db_host = "db-wmg-symfony-prd.wedmegood.infra"
db_port = 3306
db_user = "read_db_user"
db_password = "readydbuserxbgrt"
db_name = "wedmegood_symfony"
local_port = 3307  # Local forwarding port

 # if parameter==dev
        #baseurl= developmentwow
        #elif
        #url=baseurl+"/vendor-login" 

# Path to your CSV file
csv_file_path = 'C:\\Deepti\\WMG_Test_Automation\\tests\\email.csv'

with open(csv_file_path, mode='r', newline='', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    rows = [{k.strip(): v.strip() for k, v in row.items()} for row in reader]

    if not rows:
        raise ValueError("CSV file is empty or missing data.")

    if 'email' not in rows[0]:
        raise KeyError(f"Expected 'email' column, but found: {list(rows[0].keys())}")

    base_email = rows[0]['email']

# Randomize email
username, domain = base_email.split('@')
unique_suffix = str(int(time.time()))
test_email = f"{username}_{unique_suffix}@{domain}"

print("Generated Email:", test_email)

# Test email
#test_email = "testvendor303030@example.com"


# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 15)
# Get today's date for the folder name (Ensures only one folder per day)
current_date = datetime.now().strftime("%Y-%m-%d")
report_dir = os.path.join("report", current_date)

# Create the directory if it doesn't exist
os.makedirs(report_dir, exist_ok=True)

# Generate timestamp for the file name (Ensures unique files within the same folder)
timestamp = datetime.now().strftime("%H-%M-%S")  

# Define report file names
txt_filename = f"vendor_signup_{timestamp}.txt"
csv_filename = f"vendor_signup_{timestamp}.csv"

# Full file paths
txt_report_path = os.path.join(report_dir, txt_filename)
csv_report_path = os.path.join(report_dir, csv_filename)

# Get Current Timestamp
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Open TXT and CSV file
with open(txt_report_path, "w", encoding="utf-8") as report_file, open(csv_report_path, "a", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    report_file.write("Test Report\n")
    report_file.write("====================\n")
    report_file.write(f"Test execution started at: {current_time}\n\n")

    # Write CSV Header if the file is empty
    if csv_file.tell() == 0:
        csv_writer.writerow(["Timestamp", "Email", "Status", "URL", "Error"])

    try:
        report_file.write("---- Vendor Sign-Up Test ----\n")
       
        # Navigate to Signup Page
        driver.get("https://www.wedmegood.com/vendor-login")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='text-vendor pointer']"))).click()

        # Fill signup form
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='name-vendor-register']"))).send_keys("Test Vendor101")
        # Select City
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Aizawl')]"))).click()
        # Select Vendor Category
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Venues')]"))).click()

    # Fill name field
        name_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@id='name-vendor-register']")))
        name_input.send_keys("Test Vendor101")
        time.sleep(1)

        # --- Select City ---
        # Click the city dropdown
        city_container = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'Select margin-t-20') and .//div[contains(text(), 'City')]]")))
        city_container.click()
        time.sleep(1)

        # Type city name
        city_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'Select-input')]//input")))
        city_input.send_keys("Aizawl")
        time.sleep(1)
        
        # Select city and clear focus
        city_input.send_keys(Keys.DOWN)
        time.sleep(0.5)
        city_input.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # Click somewhere neutral to clear focus
        name_input.click()
        time.sleep(1)

        # --- Select Vendor Type ---
        # Click the vendor type dropdown using the exact class structure
        vendor_container = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'Select margin-t-20') and .//div[text()='Select Vendor Type*']]")))
        driver.execute_script("arguments[0].click();", vendor_container)
        time.sleep(1)

        # Find the vendor input within the second Select dropdown
        vendor_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'Select margin-t-20') and .//div[text()='Select Vendor Type*']]//input")))
        
        # Clear any existing value and type new value
        vendor_input.clear()
        vendor_input.send_keys("Venues")
        time.sleep(1)
        
        # Select vendor type
        vendor_input.send_keys(Keys.DOWN)
        time.sleep(0.5)
        vendor_input.send_keys(Keys.ENTER)
        time.sleep(1)

        # Verify selections
       # print("\nVerifying selections:")
       # city_value = driver.find_element(By.XPATH, "//div[contains(@class, 'Select margin-t-20')][1]").text
       # vendor_value = driver.find_element(By.XPATH, "//div[contains(@class, 'Select margin-t-20')][2]").text
       # print(f"Selected City: {city_value}")
      #  print(f"Selected Vendor Type: {vendor_value}")


        # Enter Email & Phone
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='email-vendor-register']"))).send_keys(test_email)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your mobile number*']"))).send_keys("9871010111")

        # Enter Password
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='password-vendor-register']"))).send_keys("Test@1234")

        # Click Sign Up
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='sign-button']"))).click()

        time.sleep(20) 
  
    
        with SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_pkey=ssh_private_key,
            ssh_private_key_password=ssh_passphrase,
            remote_bind_address=(db_host, db_port),
            local_bind_address=('192.168.1.73', local_port)
        ) as tunnel:
            print("SSH Tunnel established.")

            # Connect to the database inside the tunnel
            connection = pymysql.connect(
                host='192.168.1.73',
                port=local_port,
                user=db_user,
                password=db_password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("Database connection established.")

            
            with connection.cursor() as cursor:
                    query = """
                    SELECT otp
                    FROM otp_email oe
                    order by id desc limit 1;
                    """
                    cursor.execute(query)
                    result = cursor.fetchall()

                    if result:
                        df = pd.DataFrame(result)
                        otp = df['otp'][0]
                        print("OTP:", otp)
                        print(df.to_string(index=False))
                    else:
                        print("No records found.")

          

        # Wait for OTP input field
        otp_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter OTP*']"))).send_keys(otp)

    
        # Click Submit Button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='sign-button']"))).click()
        time.sleep(30)
        # Verify SignUp Success
        WebDriverWait(driver, 10).until(EC.url_contains("vendor-dashboard"))
        time.sleep(30)

        success_message = f"{current_time} | ✅ Sign Up successful! URL: {driver.current_url}\n"
        print(success_message)
        report_file.write(success_message)
        csv_writer.writerow([current_time, test_email, "Success", driver.current_url, ""])

    except Exception as e:
        error_message = f"{current_time} | ❌ Sign Up failed! Error: {str(e)}\n"
        print(error_message)
        report_file.write(error_message) 
        csv_writer.writerow([current_time, test_email, "Failed", "", str(e)])

    finally:
        driver.quit()
        report_file.write("\n---- End of Report ----\n")
        connection.close()
        print("Database connection closed.")
    
print(f"TXT Report saved: {txt_report_path}")
print(f"CSV Report saved: {csv_report_path}")
