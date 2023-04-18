from Helpers.CweList import CWE_IMPACTS

class Impact:
    def __init__(self, package_name, vuln_package_cwe):
        self.package_name = package_name
        self.cwe_list = vuln_package_cwe

    def impactGenerator(self):
        impactClosure = f"Since no usage of the vulnerable '{self.package_name}' library functionality was found in the application components, this issue has been classified as INFORMATIONAL.\n"

        if len(self.cwe_list) == 1:
            
            cwe = self.cwe_list[0]
            impactEntry = f"The '{self.package_name}' package has been found to contain a vulnerability that could result in severe\
                security and stability implications for your application. The nature of this vulnerability,\
                identified as '{cwe}', could lead to the following negative outcome:\n\n"
            impactBody = f"{CWE_IMPACTS[cwe]}\n"

            return impactEntry + impactBody + impactClosure

        else:
            impactEntry = f"The '{self.package_name}' package has been found to contain multiple vulnerabilities that could result\
                in severe security and stability implications for your application. The nature of these issue could lead to a range of negative outcomes, such as:\n\n"
            impactBody = ""
            for cwe in self.cwe_list:
                impactBody += f"- {CWE_IMPACTS[cwe]}\n"

            return impactEntry + impactBody + impactClosure
