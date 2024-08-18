from db.query import *

class Study:
    def __init__(self, target, correct, interpretation, analysis, summary, type):
        self.target = target
        self.correct = correct
        self.interpretation = interpretation
        self.analysis = analysis
        self.summary = summary
        self.type = type

    def to_dict(self):
        return {
            "target": self.target,
            "correct": self.correct,
            "interpretation": self.interpretation,
            "analysis": self.analysis,
            "summary": self.summary,
            "type": self.type
        }

    @staticmethod
    def from_dict(dict):
        return Study(
            dict.get("target", ""),
            dict.get("correct", ""),
            dict.get("interpretation", ""),
            dict.get("analysis", ""),
            dict.get("summary", ""),
            dict.get("type", "")
        )

def add_study(username, data):
    try:
        delete_from_collection_if_exists("study", {"username": username})
        insert_into_collection("study", data)
    except Exception as e:
        print(e)

def get_all_study(username):
    return find_from_collection("study", {"username": username})

def get_one_study(id):
    return find_from_collection("study", {"_id": id})