import json

class PackageVersionChecker:
    
    def __init__(self, package_lock_paths):
        self.packages = {}
        self.package_lock_paths = package_lock_paths
        print(self.package_lock_paths)
        self.get_package_versions()
        #self.print_packages()
        
        
    def get_package_versions(self):
        print("Getting package versions...")
        for path in self.package_lock_paths:
            with open(path+'/package-lock.json', 'r') as f:
                package_lock = json.load(f)
                
                # Retrieve all dependencies in the package-lock.json
                dependencies = package_lock.get('dependencies', {})
                
                for package_name, package_info in dependencies.items():
                    # Retrieve the version of the package
                    version = package_info.get('version')
                    
                    # If the package is not already in the dictionary, add it
                    if package_name not in self.packages:
                        self.packages[package_name] = {
                            'versions': [version]
                        }
                    else:
                        # If the package is already in the dictionary, append the version
                        if version not in self.packages[package_name]['versions']:
                            self.packages[package_name]['versions'].append(version)
        
        # Remove duplicates from versions for each package
        for package_name, package_info in self.packages.items():
            package_info['versions'] = list(set(package_info['versions']))
        
        # Remove duplicate packages
        self.packages = {k: v for k, v in self.packages.items() if v['versions']}
    
    def print_packages(self):
        # Print each package and its versions
        for package_name, package_info in self.packages.items():
            versions = ', '.join(package_info['versions'])
            print(f"{package_name}: {versions}")
