import sys
import argparse
import pkg_resources


def parse_package_name(line):
    """Parse package name from a line in the requirements file."""
    return line.strip().split("#")[0].strip().split("==")[0]


def main(requirements_file):
    """Check if all required packages are installed."""
    with open(requirements_file, "r") as f:
        required_packages = [parse_package_name(line) for line in f.readlines()]

    installed_packages = {package.key for package in pkg_resources.working_set}

    missing_packages = [
        package for package in required_packages
        if package and package.lower() not in installed_packages
    ]

    if missing_packages:
        print("Missing packages:")
        print(", ".join(missing_packages))
        sys.exit(1)
    else:
        print("All packages are installed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check if all required packages are installed.")
    parser.add_argument("requirements_file", help="Path to the requirements file.")
    args = parser.parse_args()
    main(args.requirements_file)