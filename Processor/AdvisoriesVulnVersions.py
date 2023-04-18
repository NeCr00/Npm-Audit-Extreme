import requests
from bs4 import BeautifulSoup

class AdvisoriesVulnVersions:
    
    # Method to retrieve the affected versions from the advisory page of the vulnerable package
    @staticmethod
    def get_advisories_html_affected_versions(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Obtain the Affected versions from the advisory page of the vulnerable package
        affected_version = soup.find(
            'div', {'class': 'float-left col-6 col-md-3 py-2 py-md-0 pr-2'}).text.strip()
        # Split all the elements with the affected versions by line
        vulnerable_versions = affected_version.split('\n')
        # Remove the 'Affected Version:' string which is presented as the first element
        vulnerable_versions.pop(0)

        print(vulnerable_versions)
        return vulnerable_versions
    
    
    # Method to retrieve all the affected versions for a given advisory URL
    @staticmethod
    def get_all_affected_versions(url):
        vulnerable_versions = AdvisoriesVulnVersions.get_advisories_html_affected_versions(url)
        clean_affected_versions = []
        # Construct the ranges of the affected versions
        for affected_version in vulnerable_versions:
            if ',' in affected_version and '>' in affected_version and '<' in affected_version:
                affected_version = affected_version.split(',')
                affected_version = list(
                    map(lambda version: version.replace('<', '').replace('=', '').replace('>', '').strip(' '), affected_version))
                if len(affected_version) == 2:
                    affected_version = (
                        affected_version[0]+' - '+affected_version[1]).strip(' ')
            clean_affected_versions.append(affected_version)
        return clean_affected_versions
    
    
    # Method to retrieve all the affected versions for a list of advisory URLs
    @staticmethod
    def getAdvisoriesOverallAffectedVersions(advisories_urls):
        affected_version_range = []
        for advisory_url in advisories_urls:
            resulted_versions = AdvisoriesVulnVersions.get_all_affected_versions(advisory_url)
            for affected_version in resulted_versions:
                # Check if the affected_version is already present in the affected_version_range
                if affected_version not in affected_version_range:
                    affected_version_range.append(affected_version)
        print(affected_version_range)


AdvisoriesVulnVersions.getAdvisoriesOverallAffectedVersions(["https://github.com/advisories/GHSA-q2c6-c6pm-g3gh","https://github.com/advisories/GHSA-g9r4-xpmj-mj65","https://github.com/advisories/GHSA-2cf5-4w76-r9qv","https://github.com/advisories/GHSA-f52g-6jhx-586p"])