6️⃣ SETUP.md
# ⚙️ Setup Instructions

1. Clone the repository:

```bash
git clone <repo-url>
cd AuthVault
```

2. Create a virtual environment:
``` bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```


4. Ensure directories exist:

```bash
mkdir -p database/logs
mkdir -p password_policy_tool/data/raw_logs
mkdir -p password_policy_tool/reports
```

5. Run:

AuthVault CLI:
``` bash
python3 main.py
```
Password Policy Tool CLI:

``` bash
python3 -m password_policy_tool.main check 'Password123!'
```


---

