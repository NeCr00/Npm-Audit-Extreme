import requests
from bs4 import BeautifulSoup

class AdvisoriesVulnVersions:
    
    @staticmethod
    def get_advisories_html_affected_versions(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Obtain the Affected versions from the advisory page of the vulnerable package
        affected_version = soup.find(
            'div', {'class': 'float-left col-6 col-md-3 py-2 py-md-0 pr-2'}).text.strip()
        #split all the elements with the affected versions by line
        vulnerable_versions = affected_version.split('\n')
        # Remove the 'Affected Version:' string which is presented as first element "
        vulnerable_versions.pop(0)

        return vulnerable_versions
    
    
    '''
        @staticmethod
    def get_all_affected_versions(url):
        vulnerable_versions = AdvisoriesVulnVersions.get_advisories_html_affected_versions(url)
        clean_affected_versions = []
        # Construct the ranges of the affected versions
        #If ranges are >
        for affected_version in vulnerable_versions:
            if ',' in affected_version and '>' in affected_version and '<' in affected_version:
                affected_version = affected_version.split(',')
                affected_version = list(
                    map(lambda version: version.replace('<', '').replace('=', '').replace('>', '').strip(' '), affected_version))
                if len(affected_version) == 2:

                    affected_version = (
                        affected_version[0]+' - '+affected_version[1]).strip(' ')
            clean_affected_versions.append(affected_version)
    '''





