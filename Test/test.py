class Title:
    
    def __init__(self, packageName, components):
        self.packageName = packageName
        self.components = components
        self.title = self.generateTitle()

    def ComponentProcessor(self):

        if (len(self.components) == 0):
            return "application"

        elif (len(self.components) == 1):
            return f"'{self.components[0]}' Component"

        elif (len(self.components) >= 2):
            components_title = f"'{self.components[0]}'"
            
            for component in range(1,len(self.components)-1):
                
                components_title += f", '{self.components[component]}'"

            components_title += f" and '{self.components[len(self.components)-1]}' Components"

        return components_title

    def generateTitle(self):

        title = f"Vulnerable third-party library '{self.packageName}' in use by {self.ComponentProcessor()}"
        print(title)
        return title

import sys
sys.path.append('../CWE')

from CweList import CWE_IMPACTS
print(CWE_IMPACTS)