
from Log import Log
import json


class ExtractResults:

    def __init__(self, results):
        self.results = results
        self.processed_results = []
        self.data_processing()
        self.stats = self.calculate_vulnerabilities_stats()

    def data_processing(self):
        Log.info("Extracting results from scanning ...")
        
        try:
            for result in self.results:
                if "vulnerabilities" in result:
                    self.get_vulnerabilities(result)
                    
            Log.success("Finishing extraction of  results from scanning")
        except Exception as e:
            Log.error("Could not extract data from Scanning Results: " + str(e))

    def get_vulnerabilities(self, result):
        try:

            # Get the vulnerability field containing the actual results
            vulnerabilities = result["vulnerabilities"]
            # Extract all the vulnerable packages and their informations
            vuln_packages = self.get_packages_name(vulnerabilities)
            for package in vuln_packages:
                self.get_attributes(vulnerabilities[package])

        except Exception as e:
            Log.error('No vulnerabilities available')
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
        extracted_data["via"], extracted_data["direct"] = self.getVulnerabilityDetails(
            package["via"], package["name"])

        # save the results
        self.processed_results.append(extracted_data)

    def getVulnerabilityDetails(self, vuln_details, package_name=None):
        vuln_details_list = []
        is_direct = False

        try:
            for vuln_detail in vuln_details:
                vuln = {}

                if "title" in vuln_detail:
                    # Get the name of the vulnerability
                    vuln["title"] = vuln_detail["title"]
                    # Get the severity of the vulnerability
                    vuln["severity"] = vuln_detail["severity"]
                    # Get the url of the vulnerability
                    vuln["url"] = vuln_detail["url"]
                    # Get CWE of the vulnerability
                    vuln["cwe"] = vuln_detail["cwe"]

                    # Check if the vulnerability is direct
                    is_direct = True

                    # Append the information to array
                    vuln_details_list.append(vuln)

            if is_direct:
                return (vuln_details_list, True)
            else:
                return (vuln_details, False)

        except Exception as e:
            Log.error(
                f'No Details available for package: {package_name}. Manual Inspection is required')
            return ([], False)


    def calculate_vulnerabilities_stats (self):
        
        
        for result in self.results:
            
            metadata = result["metadata"]["vulnerabilities"]    
            print(metadata)
        
        