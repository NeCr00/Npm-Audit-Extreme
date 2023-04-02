from results import results
from audit_code import audit_code
from vulnerability_checker import vulnerability_checker
from packages_version_checker import PackageVersionChecker
from log import Log
import json
import sys


def getUserArguments():
    if len(sys.argv) != 2:
        Log.error("Usage: python3 main.py <path_to_project>")
        exit(1)

    return sys.argv[1]


def main():
    # Get path for project from command line argument
    project_path = getUserArguments()
    # Get the results from the scanner
    scanner_result = results(project_path)
    # Print the results
    # json_results = json.dumps(scanner_result.processed_results, indent=4)

    auditCode = audit_code(project_path)
    package_versions = PackageVersionChecker(auditCode.auditable_paths)
    
    vulnerability_checker(scanner_result.processed_results,
                          package_versions.packages)
 


if __name__ == '__main__':
    main()
