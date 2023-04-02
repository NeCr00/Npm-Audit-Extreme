import os
import sys
import subprocess
import json
from log import Log


class audit_code:

    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.delete_authorization()
        self.auditable_paths = self.find_auditable_paths()
        self.results =self.start_audit()

    def delete_authorization(self):
        try:
            for root, dirs, files in os.walk(self.project_dir):
                for file in files:
                    if file == '.npmrc':
                        os.remove(os.path.join(root, file))
                        Log.info('Removed .npmrc file from %s/%s' %
                                 (root, file))
        except Exception as e:
            Log.error(f"Error deleting .npmrc file: {e}")
            sys.exit(1)

    def find_auditable_paths(self):
        auditable_paths = []
        for root, dirs, files in os.walk(self.project_dir):
            for file in files:
                if file == 'package-lock.json':
                    auditable_paths.append(root)

        if len(auditable_paths) == 0:
            Log.error('No package-lock.json found in %s' % self.project_dir)
            sys.exit(1)

        return auditable_paths

    def start_audit(self):
        results_audit = []
        for directory in self.auditable_paths:
            try:
                result = subprocess.run(
                    ['npm', 'audit', '--json'], cwd=directory, capture_output=True, text=True)
                results_audit.append(result.stdout)
                Log.info('Finished auditing %s/package-lock.json' % directory)
            except subprocess.CalledProcessError:
                print(f'Error running npm audit in {directory}')

        json_results = [json.loads(result) for result in results_audit]
        return json_results
        #print(json.dumps(json_results))


    def get_results_json(self):
        return json.dumps(self.results)