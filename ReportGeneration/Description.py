from Helpers.CVEFinder import CVEFinder


class Description():

    def __init__(self, data, title_obj):
        self.components_affected = title_obj.components_affected
        self.data = data
        self.advisoriesUrl = self.getAllAdvisoriesUrl()
        self.description = self.generateDescription()

    def VulnVersionText(self):
        versionText = ""

        if len(self.data['vuln_version_found']) == 1:
            return f"{self.data['vuln_version_found'][0]}"

        for version in range(0, len(self.data['vuln_version_found'])-1):
            versionText += f"{self.data['vuln_version_found'][version]}, "

        versionText += f"{self.data['vuln_version_found'][len(self.data['vuln_version_found'])-1]}"

        return versionText

    def descriptionOfVulnerabilities(self):
        
        getDescriptions = CVEFinder.get_cve_descriptions_async(self.advisoriesUrl)
        
        if len(self.data['via']) == 1:

            vuln_details = self.data['via'][0]

            description = f"The known vulnerability is named: {vuln_details['title']} - {vuln_details['url']}."
            description += f"Below is a summary of the detected vulnerability: \n\n"
            description += f"- Title: {vuln_details['title']}\n"
            description += f"- Advisory Url: {vuln_details['url']}\n"
            description += f"- Description: {getDescriptions[0]}\n"

        else:
            description = f"The security analysis of the installed package has revealed the presence of multiple vulnerabilities within the software. These vulnerabilities affect the package and could potentially lead to various security risks."
            description += f"\n\nBelow is a summary of each detected vulnerability:\n\n"
            
            
            
            for i, vuln_detail in enumerate(self.data['via'], start=1):
                description += f"Vulnerability {i}:\n"
                description += f"- Title: {vuln_detail['title']}\n"
                description += f"- URL: {vuln_detail['url']}\n"
                description += f"- Description: {getDescriptions[i]}\n\n"

        return description

    def generateDescription(self):

        if len(self.data["vuln_version_found"]) > 1:

            description_entry = f"The team has determined that multiple versions of {self.data['package_name']} library was being used in the {self.components_affected} of the application."
            description_body = f"The versions of the used package are '{self.VulnVersionText()}' while the know vulnerable versions are '{self.data['vuln_version_found']}'"
            description_end = self.descriptionOfVulnerabilities()

        else:

            description_entry = f"The team has determined that a vulnerable version of {self.data['package_name']} library was being used in the {self.components_affected} of the application."
            description_body = f"The version of the used package is '{self.VulnVersionText()}' while the know vulnerable versions are '{self.data['vuln_version_found']}'."
            description_end = self.descriptionOfVulnerabilities()
        
        return description_entry+description_body+description_end

    def getAllAdvisoriesUrl(self):
        
        advisories_url = []
        for url in self.data["via"]:
            advisories_url.append(url["url"])
        
        return advisories_url