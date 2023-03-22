import os
import sys
import subprocess

class audit_code:
    
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.delete_authorization()
        self.auditable_paths = self.find_auditable_paths() 
        self.start_audit()
        
        
    def delete_authorization(self):
        for root,dirs,files in os.walk(self.project_dir):
            for file in files:
                if file =='.npmrc':
                    os.remove(os.path.join(root,file))
    
    
    def find_auditable_paths(self):
        auditable_paths = []
        for root,dirs,files in os.walk(self.project_dir):
            for file in files:
                if file == 'package-lock.json':
                    auditable_paths.append(root)
        return auditable_paths
    
    
    def start_audit (self):
        
        results_audit = []
        
        for directory in self.auditable_paths:
            try:
                result = subprocess.run(['npm', 'audit', '--json'], cwd=directory, capture_output=True, text=True)
                results_audit.append(result.stdout)
            except subprocess.CalledProcessError:
                print(f'Error running npm audit in {directory}')
                
        print(results_audit)