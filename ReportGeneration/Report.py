from Log.Log import Log
from ReportGeneration.Title import Title
from ReportGeneration.Description import Description
from ReportGeneration.Impact import Impact
from ReportGeneration.Recommendation import Recommendation

class Report:

    def __init__(self,data):
        self.title = Title(data['package_name'],["test"])
        self.description = Description(data,self.title)
        # self.impact = Impact()
        # self.recommendation = Recommendation.get_recommendation()
        print(self.title.title,self.description.description)