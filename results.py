from audit_code import audit_code
from log import Log
import json


class results:

    def __init__(self, project_path):
        self.scanner = audit_code(project_path)
        self.processed_results = []
        self.data_processing()

    def data_processing(self):
        for result in self.scanner.results:
            if "vulnerabilities" in result:
                self.get_extracted_data(result)

    def get_extracted_data(self, package_data):
        try:

            # Get the vulnerability field containing the actual results
            vulnerabilities = package_data["vulnerabilities"]
            # Extract all the vulnerable packages and their informations
            vuln_packages = self.get_packages_name(vulnerabilities)
            for package in vuln_packages:
                self.get_attributes(vulnerabilities[package])

        except Exception as e:
            # Log.info('No vulnerabilities available')
            return

    def get_packages_name(self, vulnerabilities):
        vuln_packages = []
        for vulnerability in vulnerabilities:
            vuln_packages.append(vulnerability)

        # print(vuln_packages)
        return vuln_packages

    def get_attributes(self, package):
        extracted_data = {}

        # Get the name of the vulnerable package
        extracted_data["package_name"] = package["name"]
        # Get the version of the vulnerable package
        extracted_data["vul_version"] = package["range"]
        # Get overall Severity of the vulnerability
        extracted_data["overall-severity"] = package["severity"]
        # Get the description of the vulnerabilities which affect this package
        extracted_data["via"] = self.getVulnerabilityDetails(package["via"])
        # save the results
        self.processed_results.append(extracted_data)

    def getVulnerabilityDetails(self, vuln_details):
        vuln_details_list = []

        try:
            for vuln_detail in vuln_details:
                vuln = {}
                # Get the name of the vulnerability
                vuln["title"] = vuln_detail["title"]
                # Get the severity of the vulnerability
                vuln["severity"] = vuln_detail["severity"]
                # Get the url of the vulnerability
                vuln["url"] = vuln_detail["url"]
                # Append the information to array
                vuln_details_list.append(vuln)
            return vuln_details_list

        except Exception as e:
            Log.info('No Description available')
            return []

