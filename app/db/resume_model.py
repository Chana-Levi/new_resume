from bson.objectid import ObjectId


class ResumeModel:
    def __init__(self, db):
        self.resumes = db['resumes']

    def add_resume(self, candidate_id, job_id, full_text_resume, extract_resume, link):
        resume = {
            "candidate_id": ObjectId(candidate_id),
            "job_id": ObjectId(job_id),
            "full_text_resume": full_text_resume,
            "extract_resume": extract_resume,
            "resume_link": link
        }
        return self.resumes.insert_one(resume).inserted_id

    def update_resume(self, resume_id, extract_resume_data):
        return self.resumes.update_one(
            {"_id": ObjectId(resume_id)},
            {"$set": {"extract_resume": extract_resume_data, "is_extracted_updated": True}}
        )

    def update_resume_by_id_and_job(self, candidate_id, job_id, full_text_resume, extract_resume, link):
        return self.resumes.update_one(
            {'candidate_id': ObjectId(candidate_id), 'job_id': ObjectId(job_id)},
            {'$set': {
                'full_text_resume': full_text_resume,
                'extract_resume': extract_resume,
                'resume_link': link
            }}
        )

    def get_resume(self, resume_id):
        return self.resumes.find_one({"_id": ObjectId(resume_id)})

    def get_resumes_by_job_id(self, job_id):
        return list(self.resumes.find({"job_id": ObjectId(job_id)}))

    def delete_resume(self, resume_id):
        return self.resumes.delete_one({"_id": ObjectId(resume_id)})

    def find_resume(self, candidate_id, job_id):
        return self.resumes.find_one({'candidate_id': ObjectId(candidate_id), 'job_id': ObjectId(job_id)})