from Processor.ExtractResults import ExtractResults
from Scan.AuditCode import AuditCode
from Processor.VulnerabilityProcessor import VulnerabilityProcessor
from Scan.PackagesVersions import PackagesVersions
from Log import Log
import sys
import json

def getUserArguments():
    if len(sys.argv) != 2:
        Log.error("Usage: python3 main.py <path_to_project>")
        exit(1)

    return sys.argv[1]


def main():
    # Get path for project from command line argument
    project_path = getUserArguments()
    
# ----------------------------- Scan Procedure ------------------------------------
    # Iniztialize the Npm audit Scan
    Scanner = AuditCode(project_path)
    
    #Get all the dependencies (packages) that used in the project
    ExtractedPackagesVersions = PackagesVersions(Scanner.auditable_paths)
#----------------------------------------------------------------------------------
    
#----------------------------- Data Processing -----------------------------
    #Extract the vital information from the Npm audit scan results
    ExtractedResults = ExtractResults(Scanner.results)
    
    #Find the exact vulnerable versions that are present in the project
    #npm audit provides only the vulnerable range of veersion and not the exact vulnerable
    #version that are found in the project
    VulnerabilityComparator = VulnerabilityProcessor(ExtractedResults.processed_results, ExtractedPackagesVersions.packages)
    print(ExtractedResults.stats)
    
if __name__ == '__main__':
    main()


