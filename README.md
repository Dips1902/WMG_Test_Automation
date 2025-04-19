# 🧪 WMG Test Automation

Automation scripts to test the **vendor signup flow** and other flows on [WedMeGood](https://www.wedmegood.com).  
This includes frontend automation using **Selenium**, and OTP fetching via **MySQL + SSH Tunnel**.

---

## 📁 Project Structure

```
WMG_Test_Automation/
├── tests/                  # Test cases
│   └── test_vendor_signup.py
├── utils/                  # Reusable utility functions
│   └── db_utils.py
├── requirements.txt        # Python dependencies
├── run_tests.bat           # Quick test runner
├── README.md               # Project documentation
└── .gitignore              # Ignored files/folders
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/WMG_Test_Automation.git
cd WMG_Test_Automation
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate       # For Windows
# OR
source venv/bin/activate    # For macOS/Linux
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Tests

You can run all tests using:

```bash
python tests/run_tests.py
```

Or run a specific file like:

```bash
python tests/test_vendor_signup.py
```

---

## 🔐 Database Access (OTP Fetching)

- We use an SSH tunnel to securely access the production DB.
- The credentials and keys are not committed to the repo.
- To update or use new queries, edit `utils/db_utils.py`.

---

## 🛠 Tools & Libraries

- [Selenium](https://selenium.dev/) – Browser automation
- [PyMySQL](https://pymysql.readthedocs.io/) – MySQL access
- [SSHTunnel](https://pypi.org/project/sshtunnel/) – For secure DB connection
- [pytest](https://docs.pytest.org/) – For running tests

---

## 📌 Notes

- Python 3.12 or higher is recommended
- Do not commit environment files or secrets
- Use `.gitignore` to keep the repo clean

---

## 📡 Jenkins Integration

To run these scripts in Jenkins:
- Pull the repo
- Set up Python & virtual environment
- Install `requirements.txt`
- Run with `python tests/run_tests.py`

Let us know if you'd like a full Jenkinsfile example.

---

## 🙌 Contributing

Feel free to raise issues or contribute with PRs.

---# WMG_Test_Automation
WedMeGood Automation Scripts
