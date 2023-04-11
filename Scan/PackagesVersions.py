import json
from Log import Log

"""
    This file obtains a list of all the paths that the package-lock.json files are presented in the project.
    Afterwards, the class is extracting all the dependencies from the package-lock.json files along with their versions
    removing the duplicate versions. Lastly, the obtained results will help to distinguished the exact versions that are vulnerable
    for the corresponding dependencies (npm audit doesn't specify which vulnerable versions are presented).
"""


class PackagesVersions:

    def __init__(self, package_lock_paths):
        # initialize the instance variables
        self.packages = {}
        self.package_lock_paths = package_lock_paths
        # call the get_package_versions method to retrieve the package versions
        self.get_package_versions()

    def get_package_versions(self):
        Log.info("Getting packages versions used in project ...")
        try:
            # iterate through the package lock paths
            for path in self.package_lock_paths:
                with open(path+'/package-lock.json', 'r') as f:
                    # load the package-lock.json file as a Python object
                    package_lock = json.load(f)

                    # Retrieve all dependencies in the package-lock.json
                    dependencies = package_lock.get('dependencies', {})

                    # iterate through the dependencies and retrieve the version of each package
                    for package_name, package_info in dependencies.items():
                        version = package_info.get('version')

                        # If the package is not already in the dictionary, add it
                        if package_name not in self.packages:
                            self.packages[package_name] = {
                                'versions': [version]
                            }
                        else:
                            # If the package is already in the dictionary, append the version
                            if version not in self.packages[package_name]['versions']:
                                self.packages[package_name]['versions'].append(
                                    version)

            # Remove duplicates from versions for each package
            for package_name, package_info in self.packages.items():
                package_info['versions'] = list(
                    set(package_info['versions']))
            
            Log.success("Finished getting packages versions used in project.")
            
        except Exception as e:
            Log.error('Cannot get the package versions: ' + str(e))

        # Remove duplicate packages
        self.packages = {k: v for k,
                         v in self.packages.items() if v['versions']}

    def print_packages(self):
        # Print each package and its versions
        for package_name, package_info in self.packages.items():
            versions = ', '.join(package_info['versions'])
            print(f"{package_name}: {versions}")
