import argparse
from password_policy_tool.logs.log_analyzer import LogAnalyzer
from password_policy_tool.password_policies_manager.password_policies_manager import PasswordPolicy

def main():
    parser = argparse.ArgumentParser(description="Password Policy Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Check Password
    parser_check = subparsers.add_parser("check", help="Check a password against policy")
    parser_check.add_argument("password", type=str, help="Password to check")

    # Generate Password
    parser_generate = subparsers.add_parser("generate", help="Generate a new password")
    parser_generate.add_argument("-n", "--number", type=int, default=1, help="How many passwords")
    parser_generate.add_argument("-l", "--length", type=int, default=12, help="Length of password")

    # Show Stats
    subparsers.add_parser("stats", help="Show password log stats")

    # Export CSV
    subparsers.add_parser("export", help="Export password log summary")

    # View Logs
    parser_logs = subparsers.add_parser("logs", help="View password logs")
    parser_logs.add_argument("--mode", choices=["all", "valid", "invalid"], default="all", help="Filter: all, valid, invalid")

    args = parser.parse_args()

    pp = PasswordPolicy()
    analyzer = LogAnalyzer()

    if args.command == "check":
        valid, messages = pp.check_password(args.password)
        pp.logs.log_check(args.password, valid, messages)
        print(f"Valid: {valid}\nMessages: {messages}")

    elif args.command == "generate":
        for _ in range(args.number):
            password = pp.generate_password(args.length)
            print(f"Generated password: {password}")
            valid, msg = pp.check_password(password)
            pp.logs.log_check(password, valid, msg)

    elif args.command == "stats":
        analyzer.stats()

    elif args.command == "export":
        analyzer.export_csv()

    elif args.command == "logs":
        analyzer.check_file(mode=args.mode)

    else:
        parser.print_help()
if __name__ == "__main__":
    main()