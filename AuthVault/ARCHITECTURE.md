
```markdown
# 🏗️ AuthVault Architecture

## Directory Structure

AuthVault/
├── authvault.py # Main IAM CLI
├── modules/
│ └── auth/
│ ├── auth.py # UserManager & login
│ └── permissions.py # Role-based access control
├── modules/user/
│ ├── user.py # User object & ID generation
│ └── passwords.py # Hashing & verification
├── password_policy_tool/
│ ├── main.py # Password policy CLI
│ ├── password_policies_manager/
│ │ └── password_policies_manager.py
│ └── logs/
│ ├── logs.py
│ └── log_analyzer.py
├── database/
│ └── logs/ # All authentication logs
├── requirements.txt
└── README.md


## Module Responsibilities

- `auth.py`: Handles user registration, login, password change, and preload faculty users.  
- `permissions.py`: Maps users to groups and checks permission rights.  
- `user.py` & `passwords.py`: Secure password storage & validation, ID generation.  
- `password_policies_manager.py`: Enforces password rules, generates strong passwords.  
- `logs.py` & `log_analyzer.py`: Thread-safe logging & analysis, CSV export.  