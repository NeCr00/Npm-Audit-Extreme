import re
import requests
from bs4 import BeautifulSoup

def is_version_inside_wildcard(version_wildcard, version_str):
    version_wildcard_parts = re.split(r'\.', version_wildcard)
    version_str_parts = re.split(r'\.', version_str)

    if len(version_wildcard_parts) != len(version_str_parts):
        return False

    for i, wildcard_part in enumerate(version_wildcard_parts):
        if wildcard_part == 'x' or wildcard_part == 'X':
            continue
        elif wildcard_part != version_str_parts[i]:
            return False

    return True

# Function to remove alpha, beta, and rc version identifiers from a version string
def clean_version(version):
    version = re.sub(r'(-alpha|-beta|-rc)[^ ]*', '', version)
    return version

# Function to convert a version string into a tuple of integers
def version_to_tuple(version):
    if not version:
        return (0, 0, 0)
    version_numbers = version.split(".")[:3]
    return tuple(map(int, version_numbers))

# Function to check if a given version is vulnerable given a vulnerable version range
def is_vulnerable(version, vul_version):
    # Clean the input version and convert it to a tuple
    clean_version_number = version_to_tuple(clean_version(version))
    
    # Clean the vulnerable version range
    vul_version = clean_version(vul_version)

    # Split the vulnerable version range into individual ranges
    ranges = re.split(r'\s*\|\|\s*', vul_version)
    print(f'range {ranges}')
    # Loop through each range and check if the version is within that range
    for range_str in ranges:
        if '-' in range_str:
            # Range specified with a dash
            bounds = [x.strip() for x in range_str.split('-')]
            if len(bounds) == 2:
                # Convert the lower and upper bounds to tuples and check if the version is within that range
                lower, upper = [version_to_tuple(x) for x in bounds]
                if lower <= clean_version_number <= upper:
                    return True
        elif '>=' in range_str and '<' in range_str:
            # Range specified with a greater-than-or-equal-to and a less-than symbol
            lower, upper = re.findall(r'\d+\.\d+\.\d+', range_str)
            print(lower, upper)
            lower = version_to_tuple(lower.strip('><= '))
            upper = version_to_tuple(upper.strip('><= '))
            print(lower, upper)
            if lower <= clean_version_number < upper:
                return True
        elif '>' in range_str and '<=' in range_str:
            # Range specified with a greater-than and a less-than-or-equal-to symbol
            lower, upper = re.findall(r'\d+\.\d+\.\d+', range_str)
            lower = version_to_tuple(lower.strip('><= '))
            upper = version_to_tuple(upper.strip('><= '))
            if lower < clean_version_number <= upper:
                return True
        elif '<=' in range_str:
            # Range specified with a less-than-or-equal-to symbol
            upper = version_to_tuple(range_str.strip('><= '))
            if clean_version_number <= upper:
                return True
        elif '<' in range_str:
            # Range specified with a less-than symbol
            upper = version_to_tuple(range_str.strip('><= '))
            if clean_version_number < upper:
                return True
        elif '>=' in range_str:
            # Range specified with a greater-than-or-equal-to symbol
            lower = version_to_tuple(range_str.strip('><= '))
            if clean_version_number >= lower:
                return True
        elif '>' in range_str:
            # Range specified with a greater-than symbol
            lower = version_to_tuple(range_str.strip('><= '))
            if clean_version_number > lower:
                return True
        elif 'x' in range_str or 'X' in range_str:
            version = clean_version(version)
            return is_version_inside_wildcard(range_str,version)
        
    # Version is not vulnerable
    return False


def get_version ():
    url = 'https://github.com/advisories/GHSA-xvch-5gv4-984h'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Obtain the Affected verisons from the advisory page of the vulnerable package
    affected_version = soup.find(
        'div', {'class': 'float-left col-6 col-md-3 py-2 py-md-0 pr-2'}).text.strip()
    vulnerable_versions = affected_version.split('\n')
    # Remove the 'Affected Version:' string"
    vulnerable_versions.pop(0)
    
    return vulnerable_versions


vul_versions = ["1.x.0"]

for vul_version in vul_versions:
    data = get_version()
    print(data)
    result = is_vulnerable("5.7.4", '>=5.5.0 <5.7.4')
    
    print(result)
    print("---------------------")


