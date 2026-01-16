# main.py (AuthVault)

from password_policy_tool.password_policies_manager.password_policies_manager import PasswordPolicy
from password_policy_tool.logs.log_analyzer import LogAnalyzer
from modules.logs.logs import Logs
from modules.auth.auth import UserManager
from modules.auth.permissions import can_user_perform

# -------------------- Initialize --------------------
logs = Logs()              # single shared logs instance
um = UserManager()     # pass the same logs object
pp = PasswordPolicy()
loga = LogAnalyzer()

# -------------------- Main Menu --------------------
def main_menu():
    print("\n=== AuthVault ===")
    print("-" * 40)
    print("1. Admin / Department Head Login")
    print("2. User Login")
    print("3. Password Policy Menu")
    print("4. Exit")
    return input("Enter choice: ")

# -------------------- Admin Actions --------------------
def admin_actions(username):
    while True:
        print(f"\n--- Admin Menu ({username}) ---")
        print("0. Logout")
        menu_idx = 1
        actions = {}

        if can_user_perform(username, "create_user"):
            print(f"{menu_idx}. Register new user")
            actions[str(menu_idx)] = "create_user"
            menu_idx += 1
        if can_user_perform(username, "view_logs"):
            print(f"{menu_idx}. View user logs")
            actions[str(menu_idx)] = "view_logs"
            menu_idx += 1

        choice = input("Select action: ")
        if choice == "0":
            break
        elif choice in actions:
            if actions[choice] == "create_user":
                new_username = input("New username: ")
                new_password = input("New password: ")
                role = input("Role (user/admin/master_admin): ")
                role_obj = {"role": role}
                result = um.register(new_username, new_password, role_obj)
                print(result["error"] if not result["ok"] else f"{new_username} registered successfully!")
            elif actions[choice] == "view_logs":
                logs.load_logs()  # reload latest logs
                print("User logs:", logs.user_logs)
                print("Admin logs:", logs.admin_logs)
                print("Master Admin logs:", logs.master_admin_logs)
        else:
            print("Invalid option or insufficient permissions.")

# -------------------- User Actions --------------------
def user_actions(username):
    while True:
        print(f"\n--- User Menu ({username}) ---")
        print("0. Logout")
        actions = []
        idx = 1

        if can_user_perform(username, "view_employee_data"):
            actions.append((str(idx), "View employee data"))
            idx += 1
        if can_user_perform(username, "update_employee_data"):
            actions.append((str(idx), "Update employee data"))
            idx += 1

        # Password change is available for all users
        actions.append((str(idx), "Change Password"))
        change_pw_idx = str(idx)

        for act in actions:
            print(f"{act[0]}. {act[1]}")

        choice = input("Select action: ")
        if choice == "0":
            break
        elif choice == change_pw_idx:
            old_pw = input("Enter current password: ")
            new_pw = input("Enter new password: ")
            result = um.change_password(username, old_pw, new_pw)
            if result["ok"]:
                print("✅ Password changed successfully!")
            else:
                print(f"❌ {result['error']}")
        else:
            print("Feature not implemented or insufficient permissions.")

# -------------------- Password Policy Menu --------------------
def password_policy_menu():
    while True:
        print("\n--- Password Policy Menu ---")
        print("0. Back")
        print("1. Check single password")
        print("2. Check passwords from file (all)")
        print("3. Check passwords from file (valid)")
        print("4. Check passwords from file (invalid)")
        print("5. Generate passwords")
        print("6. Export logs to CSV")
        print("7. Generate stats")

        choice = input("Select option: ")

        if choice == "0":
            break
        elif choice == "1":
            pw = input("Enter password: ")
            valid, feedback = pp.check_password(pw)
            if valid:
                print("✅ Password is valid")
            else:
                print("❌ Password NOT valid:")
                for msg in feedback:
                    print(msg)
        elif choice == "2":
            loga.check_file(mode="all")
        elif choice == "3":
            loga.check_file(mode="valid")
        elif choice == "4":
            loga.check_file(mode="invalid")
        elif choice == "5":
            n = int(input("How many passwords? ") or 1)
            length = int(input("Length? ") or 12)
            for _ in range(n):
                print(pp.generate_password(length))
        elif choice == "6":
            loga.export_csv()
        elif choice == "7":
            loga.stats()
        else:
            print("Invalid option.")

# -------------------- Main CLI Loop --------------------
def main():
    # Preload faculty users with temporary passwords
    um.preload_faculty_users()

    while True:
        choice = main_menu()

        if choice in ["1", "2"]:
            username = input("Username: ")
            password = input("Password: ")
            result = um.login(username, password)

            if not result["ok"]:
                print("Login failed:", result["error"])
                continue

            user_data = um.users[username]

            # --- FORCE PASSWORD RESET ON FIRST LOGIN ---
            while user_data.get("force_reset", True):
                print("\n⚠️ You must change your temporary password before proceeding!")
                new_pw = input("Enter new password: ")
                confirm_pw = input("Confirm new password: ")
                if new_pw != confirm_pw:
                    print("❌ Passwords do not match. Try again.")
                    continue

                change_result = um.change_password(username, password, new_pw)
                if change_result["ok"]:
                    print("✅ Password changed successfully!")
                    user_data["force_reset"] = False
                    password = new_pw
                    break
                else:
                    print(f"❌ {change_result['error']}")

            # --- Role-based menu ---
            role = result["data"]["role"]["role"]
            if role in ["admin", "master_admin"]:
                admin_actions(username)
            else:
                user_actions(username)

        elif choice == "3":
            password_policy_menu()
        elif choice == "4":
            print("Exiting AuthVault. Goodbye!")
            break
        else:
            print("Invalid choice.")

# -------------------- Run CLI --------------------
if __name__ == "__main__":
    main()
