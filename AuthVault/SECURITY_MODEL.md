# 🔒 Security Model

## 1. Roles & Permissions

| Role | Capabilities |
|------|-------------|
| Master Admin | Full access, create users, view all logs |
| Admin | Department management, limited log access |
| User | Login & change password |
| TA / Restricted | View-only or limited access |

## 2. Password Policies

- Minimum 8 characters, maximum 128  
- Must include uppercase, lowercase, digit, and special character  
- Automatic password generation that always complies with policy  

## 3. Logging

- Authentication and password policy actions are logged in JSON  
- Thread-safe log writes with `Lock()`  
- Future enhancement: encrypted logs  

## 4. Future Enhancements

- Multi-Factor Authentication (MFA)  
- Log file encryption  
- Networked authentication & audit APIs  
