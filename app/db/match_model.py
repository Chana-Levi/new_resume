from bson.objectid import ObjectId


class MatchModel:
    def __init__(self, db):
        self.matches = db['matches']

    def add_match(self, candidate_id, job_id, general_requirements, mandatory_requirements, advantageous_requirements,
                  final_score, comments):
        match = {
            "candidate_id": ObjectId(candidate_id),
            "job_id": ObjectId(job_id),
            "general_requirements": general_requirements,
            "mandatory_requirements": mandatory_requirements,
            "advantageous_requirements": advantageous_requirements,
            "final_score": final_score,
            "general_system_comments": comments
        }
        return self.matches.insert_one(match).inserted_id

    def get_match(self, match_id):
        return self.matches.find_one({"_id": ObjectId(match_id)})

    def get_matches_by_job_id(self, job_id):
        return list(self.matches.find({"job_id": ObjectId(job_id)}))

    def delete_matches_by_job_id(self, job_id):
        return self.matches.delete_many({"job_id": ObjectId(job_id)})

    def delete_match_by_candidate_and_job(self, candidate_id, job_id):
        return self.matches.delete_one({
            "candidate_id": ObjectId(candidate_id),
            "job_id": ObjectId(job_id)
        })