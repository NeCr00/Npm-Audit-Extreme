import re

# Function to remove alpha, beta, and rc version identifiers from a version string
def clean_version(version):
    version = re.sub(r'(-alpha|-beta|-rc)\.?\d*', '', version)
    return version

# Function to convert a version string into a tuple of integers
def version_to_tuple(version):
    if not version:
        return (0, 0, 0)
    version_numbers = version.split(".")[:2]
    return tuple(map(int, version_numbers))

# Function to check if a given version is vulnerable given a vulnerable version range
def is_vulnerable(version, vul_version):
    # Clean the input version and convert it to a tuple
    clean_version_number = version_to_tuple(clean_version(version))
    
    # Clean the vulnerable version range
    vul_version = clean_version(vul_version)

    # Split the vulnerable version range into individual ranges
    ranges = re.split(r'\s*\|\|\s*', vul_version)

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
            lower = version_to_tuple(lower.strip('><= '))
            upper = version_to_tuple(upper.strip('><= '))
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

    # Version is not vulnerable
    return False


vul_versions = [
    "3.0.0 || 4.0.0 - 4.1.0",
    "1.0.0-rc1 - 2.1.8",
    "<0.2.1",
    "2.5.0 - 2.5.2 || 4.2.0 - 5.0.0-rc.0",
    "<5.1.2",
    "<1.3.6",
    "12.1.2-alpha.6230044c - 25.5.4",
    "12.1.1-alpha.2935e14d || 12.1.2-alpha.6230044c - 25.5.4",
    "12.1.1-alpha.2935e14d - 25.5.4",
    "10.0.2 - 25.5.0",
    "24.2.0-alpha.0 - 25.5.4",
    "21.0.0-alpha.1 - 25.5.4",
    "12.1.1-alpha.2935e14d - 25.5.4",
    "<=16.5.3",
    "<0.4.0",
    "<1.0.2 || >=2.0.0 <2.2.2",
    "0.3.0 - 1.4.1 || 2.0.0 - 2.0.1",
    "<=1.4.1",
    "<3.0.5",
    "<=0.2.3 || 1.0.0 - 1.2.5",
    "0.4.1 - 0.5.1",
    "<2.6.7",
    "<8.0.1",
    "6.5.0 - 6.5.2",
    "3.7.10 - 4.0.2",
    "<=4.4.17",
    "<4.8.1",
    "1.7.2 - 1.7.5",
    "1.3.0 - 1.3.3 || 3.3.5 - 3.3.11",
    "<11.8.5",
    "<4.1.1",
    "2.0.0 - 2.0.5",
    "2.0.0 - 2.0.5",
    "2.1.x"

]

for vul_version in vul_versions:
    print("2.1.1")
    print(vul_version)
    result = is_vulnerable("2.1.1", vul_version)
   
    print(result)
    print("---------------------")


