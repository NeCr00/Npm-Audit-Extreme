
import os
import sys
import subprocess
import json

from Log.Log import Log


class AuditCode:
    
    
    def __init__(self, project_dir):
        self.project_dir = project_dir
        # call the delete_authorization method to remove the .npmrc file
        self.delete_authorization()
        # call the find_auditable_paths method to get the auditable paths
        self.auditable_paths = self.find_auditable_paths()
        # call the start_audit method to start auditing the project directories
        self.results = self.start_audit()
        
    
    # This vital is method to remove the.npmrc file from the project directories
    def delete_authorization(self):
        Log.info("Removing.npmrc file from project directories ...")
        try:
            # traverse through the directories and remove the .npmrc file
            for root, dirs, files in os.walk(self.project_dir):
                for file in files:
                    if file == '.npmrc':
                        os.remove(os.path.join(root, file))
                        # log a message indicating the file has been removed
                        Log.info('Removed .npmrc file from %s/%s' % (root, file))
            Log.success('Removed.npmrc file from project directories')
        except Exception as e:
            # log an error message if there was an error deleting the file and exit the program
            Log.error(f"Error deleting .npmrc file: {e}")
            sys.exit(1)
    
    # method to find the auditable paths in the project directories
    def find_auditable_paths(self):
        Log.info("Finding paths to audit in project directories ...")
        auditable_paths = []
        # traverse through the directories and find the package-lock.json files
        for root, dirs, files in os.walk(self.project_dir):
            for file in files:
                if file == 'package-lock.json':
                    auditable_paths.append(root)
        Log.success("Found paths to audit in project directories")
        
        # log an error message and exit the program if no package-lock.json files were found
        if len(auditable_paths) == 0:
            Log.error('No package-lock.json found in %s' % self.project_dir)
            sys.exit(1)
        
        return auditable_paths
    
    # method to start the audit process on the auditable paths
    def start_audit(self):
        Log.info("Starting audit process ...")
        results_audit = []
        # iterate through the auditable paths and run the npm audit command
        for directory in self.auditable_paths:
            try:
                result = subprocess.run(['npm', 'audit', '--json'], cwd=directory, capture_output=True, text=True)
                results_audit.append(result.stdout)
                # log a message indicating the audit has been finished
                Log.info('Finished auditing %s/package-lock.json' % directory)
            except subprocess.CalledProcessError:
                # print an error message if there was an error running the npm audit command
                Log.error(f'Error running npm audit in {directory}')
        
        # parse the JSON results and return them
        json_results = [json.loads(result) for result in results_audit]
        Log.success("Finished auditing project directories")
        return json_results

    # method to get the audit results in JSON format
    def get_results_json(self):
        return json.dumps(self.results)
