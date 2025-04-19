import os
import pandas as pd

#  Base reports folder (update path if needed)
base_folder = "C:\\Deepti\\WMG_Test_Automation\\report"

#  Find the latest timestamped folder
def get_latest_folder(base_path):
    try:
        folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
        latest_folder = max(folders, key=lambda f: os.path.getmtime(os.path.join(base_path, f)))
        return os.path.join(base_path, latest_folder)
    except ValueError:
        return None  # No folders found

#  Get the latest folder path
latest_folder_path = get_latest_folder(base_folder)

if not latest_folder_path:
    print("❌ No timestamped folders found inside the reports directory!")
    exit()

print(f"Processing reports from: {latest_folder_path}")

#  Output file
output_file = os.path.join(latest_folder_path, "combined_report.csv")

#  List all CSV and TXT files
csv_files = [f for f in os.listdir(latest_folder_path) if f.endswith(".csv")]
txt_files = [f for f in os.listdir(latest_folder_path) if f.endswith(".txt")]

#  Initialize storage for combined data
combined_data = []

# Function to process CSV files
def process_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"⚠ Error reading {file_path}: {e}")
        return None

# Function to process TXT files
def process_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            extracted_data = [line.strip().split(" | ") for line in lines if "|" in line]
            return pd.DataFrame(extracted_data, columns=["Timestamp", "Status", "URL", "Error"])
    except Exception as e:
        print(f"⚠ Error reading {file_path}: {e}")
        return None

# Process all CSV and TXT files
for file in csv_files:
    df = process_csv(os.path.join(latest_folder_path, file))
    if df is not None:
        combined_data.append(df)

for file in txt_files:
    df = process_txt(os.path.join(latest_folder_path, file))
    if df is not None:
        combined_data.append(df)

# Combine and save final report
if combined_data:
    final_df = pd.concat(combined_data, ignore_index=True)
    final_df.to_csv(output_file, index=False)
    print(f"✅ Combined report saved: {output_file}")
else:
    print("❌ No valid reports found in the latest folder!")

