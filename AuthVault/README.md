# 📄 AuthVault — Authentication & Password Policy Toolkit

AuthVault is a modular authentication, password compliance, and audit logging toolkit designed for educational and enterprise-style security environments. It simulates Identity & Access Management (IAM), password enforcement, role-based permissions, and log analysis through a clean command-line interface (CLI).

---

## 🚀 Features

- **Identity & Access Management**
  - Username-based login
  - Role-based access (master admin, admin, user)
  - Department-level permissions

- **Password Policy Enforcement**
  - Configurable password rules
  - Password validation (`check`)
  - Secure password generation (`generate`)

- **Audit Logs & Compliance**
  - Authentication logging
  - Password policy violation tracking
  - Statistics and CSV export for compliance

- **Command-Line Interface**
  - Admin & user menus
  - Policy inspection
  - Exportable reports

---

## 💻 Setup & Usage

### 1️⃣ Setup Environment

```bash
git clone <repo-url>
cd AuthVault
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2️⃣ Run Authentication System
``` bash
python3 main.py
```

Menu options:

Admin / Department Head Login

User Login

Password Policy Menu

Exit

3️⃣ Run Password Policy Tool
``` bash
python3 -m password_policy_tool.main <command>
```

Commands:

Command	Description
check <password>	Validate a password against policy
generate	Generate a compliant password
stats	Show log stats (valid/invalid passwords)
export	Export password logs to CSV
logs	View logs (all, valid, invalid)

Examples:
``` bash
python3 -m password_policy_tool.main check 'MyPass123!'
python3 -m password_policy_tool.main generate -n 10 -l 16 # or --number 10 --length 16
python3 -m password_policy_tool.main stats
python3 -m password_policy_tool.main export
python3 -m password_policy_tool.main logs --mode valid # or --mode invalid or --mode all
```
## 🧩 Logging & Compliance

- Authentication logs: database/logs/

- Password policy logs: password_policy_tool/data/raw_logs/

- Exportable CSVs for compliance and audit reports

- 🔒 Security Notes

- Role-based access control (RBAC) with departmental restrictions

- Strong password policy enforcement

- Future plans: log encryption, MFA support, networked authentication

## 💡 Skills Highlight

This project demonstrates expertise in the following areas:

- **Python Development:** Object-oriented design, modular programming, and clean code structure.  
- **Security & Password Management:** Password validation, generation, and policy enforcement.  
- **Role-Based Access Control (RBAC):** Implementation of master_admin, admin, and user permissions.  
- **Thread-Safe Logging & Data Persistence:** Logs for all user actions stored safely in JSON files.  
- **CLI Design & User Interaction:** Fully interactive terminal interface with menus and prompts.  
- **Data Export & Analysis:** CSV exports, stats computation, and password log analysis.  
- **Project Organization & Deployment:** Clear folder hierarchy, modularized components, and reusable code.  

> This section highlights the technical competencies demonstrated throughout the AuthVault and Password Policy Tool project.
