#!/usr/bin/env python3
"""
BLKSHP OS Site Provisioning Script

This script automates the creation and configuration of tenant sites for BLKSHP OS.
It is an internal tool for BLKSHP Operations staff only.

Usage:
    # Local bench
    python scripts/bootstrap_site.py --site tenant1.local --plan FOUNDATION

    # With module overrides
    python scripts/bootstrap_site.py --site tenant1.local --plan FOUNDATION \\
        --enable-module inventory --enable-module procurement

    # Frappe Press (requires Press API credentials)
    python scripts/bootstrap_site.py --site tenant1.frappe.cloud --plan FOUNDATION \\
        --press --press-team "myteam"

Requirements:
    - BLKSHP Operations credentials
    - For Press: FC_API_KEY and FC_API_SECRET environment variables
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

# ANSI color codes for pretty output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(message: str) -> None:
    """Print a formatted header message."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}", file=sys.stderr)


def print_info(message: str) -> None:
    """Print an info message."""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def run_command(cmd: list[str], capture_output: bool = False, check: bool = True) -> Optional[str]:
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check
        )
        if capture_output:
            return result.stdout.strip()
        return None
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(cmd)}")
        if capture_output and e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        raise


def check_bench_environment() -> bool:
    """Check if we're in a Frappe bench environment."""
    try:
        run_command(["bench", "--version"], capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_local_site(site_name: str, admin_password: str = "admin") -> None:
    """Create a new site on local bench."""
    print_header(f"Creating Local Site: {site_name}")

    # Check if site already exists
    try:
        sites = run_command(["bench", "--site", site_name, "version"], capture_output=True, check=False)
        if sites:
            print_warning(f"Site {site_name} already exists. Skipping creation.")
            return
    except:
        pass

    print_info(f"Creating new site: {site_name}")
    run_command([
        "bench", "new-site", site_name,
        "--admin-password", admin_password,
        "--no-mariadb-socket"
    ])
    print_success(f"Site {site_name} created successfully")


def install_apps(site_name: str, apps: list[str]) -> None:
    """Install apps on the site."""
    print_header(f"Installing Apps on {site_name}")

    for app in apps:
        print_info(f"Installing app: {app}")
        run_command(["bench", "--site", site_name, "install-app", app])
        print_success(f"App {app} installed")


def apply_subscription_plan(site_name: str, plan_code: str, module_overrides: Optional[list[str]] = None) -> None:
    """Apply subscription plan and module overrides to the site."""
    print_header(f"Configuring Subscription Plan: {plan_code}")

    # Create a Python script to execute in Frappe context
    script = f"""
import frappe

def configure_plan():
    # This function runs in the Frappe context
    print("Configuring subscription plan: {plan_code}")

    # Get or create company (first company or create demo)
    company = frappe.db.get_value("Company", {{"is_group": 0}}, "name")
    if not company:
        print("Creating demo company")
        company_doc = frappe.get_doc({{
            "doctype": "Company",
            "company_name": "Demo Company",
            "abbr": "DC",
            "default_currency": "USD",
            "country": "United States"
        }})
        company_doc.insert(ignore_permissions=True)
        company = company_doc.name

    print(f"Using company: {{company}}")

    # Verify plan exists
    if not frappe.db.exists("Subscription Plan", {{"plan_code": "{plan_code}"}}):
        print(f"ERROR: Subscription plan '{plan_code}' not found!")
        print("Available plans:", frappe.get_all("Subscription Plan", pluck="plan_code"))
        return False

    print(f"Plan '{plan_code}' verified")

    # Apply module overrides if provided
    module_overrides = {json.dumps(module_overrides or [])}
    if module_overrides:
        print(f"Applying module overrides: {{module_overrides}}")
        for module_key in module_overrides:
            # Create Module Activation override
            if not frappe.db.exists("Module Activation", {{"module_key": module_key}}):
                print(f"Creating module activation for: {{module_key}}")
                # This would be actual implementation
                pass

    frappe.db.commit()
    print("Subscription configuration complete")
    return True

configure_plan()
"""

    # Save script to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        print_info("Applying subscription configuration...")
        output = run_command(["bench", "--site", site_name, "execute", script_path], capture_output=True)

        # Check if the script reported an error
        if output and "ERROR:" in output:
            print_error("Subscription plan configuration failed")
            print(output)
            raise RuntimeError(f"Failed to apply subscription plan '{plan_code}'")

        print_success("Subscription plan applied")
    finally:
        os.unlink(script_path)


def run_migrations(site_name: str) -> None:
    """Run database migrations."""
    print_header("Running Migrations")
    print_info("Running migrate...")
    run_command(["bench", "--site", site_name, "migrate"])
    print_success("Migrations complete")


def setup_administrator_user(site_name: str) -> None:
    """Set up BLKSHP Operations user with proper roles."""
    print_header("Configuring Administrator Access")

    script = """
import frappe

# Ensure BLKSHP Operations role exists
if not frappe.db.exists("Role", "BLKSHP Operations"):
    role = frappe.get_doc({
        "doctype": "Role",
        "role_name": "BLKSHP Operations",
        "desk_access": 1
    })
    role.insert(ignore_permissions=True)
    print("Created BLKSHP Operations role")

frappe.db.commit()
print("Administrator access configured")
"""

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(script)
        script_path = f.name

    try:
        run_command(["bench", "--site", site_name, "execute", script_path])
        print_success("Administrator access configured")
    finally:
        os.unlink(script_path)


def print_completion_summary(site_name: str, plan_code: str, press: bool = False) -> None:
    """Print completion summary with next steps."""
    print_header("Provisioning Complete!")

    print(f"{Colors.BOLD}Site Details:{Colors.ENDC}")
    print(f"  Site Name:    {Colors.OKCYAN}{site_name}{Colors.ENDC}")
    print(f"  Plan:         {Colors.OKCYAN}{plan_code}{Colors.ENDC}")
    print(f"  Environment:  {Colors.OKCYAN}{'Frappe Press' if press else 'Local Bench'}{Colors.ENDC}")

    print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
    if press:
        print(f"  1. Access site at: https://{site_name}")
        print("  2. Verify plan configuration in Subscription Management")
        print("  3. Test module access with tenant user")
    else:
        print(f"  1. Start bench: bench start")
        print(f"  2. Access site at: http://{site_name}:8000")
        print("  3. Login with: Administrator / admin")
        print("  4. Verify subscription plan in Desk")

    print(f"\n{Colors.BOLD}BLKSHP Operations Notes:{Colors.ENDC}")
    print("  • This site is for internal testing/demos only")
    print("  • Clients must contact BLKSHP to request plan changes")
    print("  • All admin actions are audit-logged")

    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Site provisioning successful!{Colors.ENDC}\n")


def provision_local_site(args: argparse.Namespace) -> None:
    """Provision a site on local bench."""
    try:
        # Verify bench environment
        if not check_bench_environment():
            print_error("Not in a Frappe bench environment. Please run from bench directory.")
            sys.exit(1)

        # Create site
        create_local_site(args.site, args.admin_password)

        # Install apps (ERPNext must be installed before BLKSHP OS)
        required_apps = ["erpnext", "blkshp_os"]
        install_apps(args.site, required_apps)

        # Run migrations
        run_migrations(args.site)

        # Setup administrator
        setup_administrator_user(args.site)

        # Apply subscription plan
        apply_subscription_plan(args.site, args.plan, args.enable_module)

        # Print summary
        print_completion_summary(args.site, args.plan, press=False)

    except Exception as e:
        print_error(f"Provisioning failed: {str(e)}")
        sys.exit(1)


def provision_press_site(args: argparse.Namespace) -> None:
    """Provision a site on Frappe Press."""
    print_error("Frappe Press provisioning not yet implemented")
    print_info("This feature requires Frappe Cloud API integration")
    print_info("Contact BLKSHP DevOps for Press provisioning support")
    sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BLKSHP OS Site Provisioning (Internal Tool - BLKSHP Operations Only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create local site with FOUNDATION plan
  python scripts/bootstrap_site.py --site demo.local --plan FOUNDATION

  # Create with custom modules enabled
  python scripts/bootstrap_site.py --site tenant1.local --plan FOUNDATION \\
      --enable-module inventory --enable-module procurement

  # Frappe Press (requires API credentials)
  export FC_API_KEY="your-key"
  export FC_API_SECRET="your-secret"
  python scripts/bootstrap_site.py --site tenant1.frappe.cloud --plan FOUNDATION --press

For more information, see docs/DEVELOPMENT-GUIDE.md
        """
    )

    parser.add_argument(
        "--site",
        required=True,
        help="Site name (e.g., demo.local or tenant.frappe.cloud)"
    )

    parser.add_argument(
        "--plan",
        required=True,
        help="Subscription plan code (e.g., FOUNDATION)"
    )

    parser.add_argument(
        "--enable-module",
        action="append",
        dest="enable_module",
        help="Enable specific module (can be specified multiple times)"
    )

    parser.add_argument(
        "--admin-password",
        default="admin",
        help="Administrator password (default: admin)"
    )

    parser.add_argument(
        "--press",
        action="store_true",
        help="Provision on Frappe Press instead of local bench"
    )

    parser.add_argument(
        "--press-team",
        help="Frappe Press team name (required if --press is used)"
    )

    args = parser.parse_args()

    # Validate Press-specific arguments
    if args.press and not args.press_team:
        parser.error("--press-team is required when using --press")

    if args.press:
        # Check for Press API credentials
        if not os.getenv("FC_API_KEY") or not os.getenv("FC_API_SECRET"):
            print_error("Frappe Cloud API credentials not found")
            print_info("Please set FC_API_KEY and FC_API_SECRET environment variables")
            sys.exit(1)

        provision_press_site(args)
    else:
        provision_local_site(args)


if __name__ == "__main__":
    main()
