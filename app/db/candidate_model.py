from bson.objectid import ObjectId


class CandidateModel:
    def __init__(self, db):
        self.candidates = db['candidates']

    def add_candidate(self, email, name):
        candidate = {
            "email": email,
            "name": name,
        }
        return self.candidates.insert_one(candidate).inserted_id

    def get_candidate(self, candidate_id):
        return self.candidates.find_one({"_id": ObjectId(candidate_id)})

    def find_candidate(self, name, email):
        return self.candidates.find_one({'email': email, 'name': name})