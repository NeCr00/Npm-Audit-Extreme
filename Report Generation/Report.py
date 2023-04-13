from Log.Log import Log
from Title import Title

class Report:

    def __init__(self,data):
        self.title = Title(data["package_name"],data["components"])
        self.description = Description()
        