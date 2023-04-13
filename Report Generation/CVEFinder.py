import requests
from bs4 import BeautifulSoup
import concurrent.futures

class CVEFinder:
    # Static method that takes an advisory URL as input and returns a link to a related CVE entry, if one exists
    @staticmethod
    def get_cve_link(advisory_url):
        with requests.Session() as session:
            response = session.get(advisory_url)
        soup = BeautifulSoup(response.content, 'lxml')
        # Look for a link with an href that starts with 'https://nvd.nist.gov/vuln/detail/CVE', which indicates a CVE entry
        cve_link = soup.find('a', href=lambda href: href and href.startswith('https://nvd.nist.gov/vuln/detail/CVE'))
        if cve_link:
            return cve_link['href']
        else:
            return None
    
    # Static method that takes an advisory URL as input and returns the CVE entry's description, if it exists
    @staticmethod
    def get_cve_description(advisory_url):
        cve_url = CVEFinder.get_cve_link(advisory_url)
        if not cve_url:
            return None
        with requests.Session() as session:
            response = session.get(cve_url)
        soup = BeautifulSoup(response.content, 'lxml')
        # Look for a <p> tag with a 'data-testid' attribute set to 'vuln-description', which contains the CVE entry's description
        description = soup.find('p', {'data-testid': 'vuln-description'})
        if description:
            return description.text
        else:
            return None
    
    # Static method that takes a list of advisory URLs as input and returns a list of the corresponding CVE entry descriptions, obtained asynchronously using threads
    @staticmethod
    def get_cve_descriptions_async(advisory_urls):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(CVEFinder.get_cve_description, url) for url in advisory_urls]
            results = []
            # As each future completes, append its result to the results list
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
        return results


print(CVEFinder.get_cve_descriptions_async(["https://github.com/advisories/GHSA-qgmg-gppg-76g5","https://github.com/advisories/GHSA-qgmg-gppg-76g5","https://github.com/advisories/GHSA-qgmg-gppg-76g5","https://github.com/advisories/GHSA-qgmg-gppg-76g5"]))