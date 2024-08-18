from db.query import *
from bson import ObjectId

class Study:
    def __init__(self, target, cord, correct, interpretation, analysis, type, username):
        self.target = target
        self.correct = correct
        self.cord = cord
        self.interpretation = interpretation
        self.analysis = analysis
        self.type = type
        self.username = username

    def to_dict(self):
        return {
            "target": self.target,
            "cord": self.cord,
            "correct": self.correct,
            "interpretation": self.interpretation,
            "analysis": self.analysis,
            "type": self.type,
            "username": self.username
        }

    @staticmethod
    def from_dict(dict):
        return Study(
            dict.get("target", ""),
            dict.get("cord", ""),
            dict.get("correct", ""),
            dict.get("interpretation", ""),
            dict.get("analysis", ""),
            dict.get("type", ""),
            dict.get("username", "")
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
    return find_from_collection("study", {"_id": ObjectId(id)})
