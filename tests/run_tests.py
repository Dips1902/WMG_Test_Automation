import os
import subprocess
import time

# Path to the test scripts directory
tests_folder = "C:\\Deepti\\WMG_Test_Automation\\tests"

# List of test scripts (Modify if needed)
test_scripts = [
    "test_vendor_login_failure_emptycreds.py",
    "test_vendor_login_failure_wrongemail.py",
    "test_vendor_login_failure_wrongpwd.py",
    "test_vendor_login_success.py",
    "test_vendor_signup.py",
]

# Run test scripts one by one
for script in test_scripts:
    script_path = os.path.join(tests_folder, script)
    
    if os.path.exists(script_path):
        print(f" Running: {script} ...")
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        
        # Print output & errors if any
        print(result.stdout)
        if result.stderr:
            print(f"⚠ ERROR in {script}:\n{result.stderr}")
        
        # Small delay to avoid overlap (optional)
        time.sleep(2)
    else:
        print(f"Script not found: {script}")

#  Run `combine_reports.py`
combine_script = os.path.join(tests_folder, "combine_reports.py")

if os.path.exists(combine_script):
    print("Running combine_reports.py ...")
    result = subprocess.run(["python", combine_script], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"⚠ ERROR in combine_reports.py:\n{result.stderr}")
else:
    print(" combine_reports.py not found!")
