from bson.objectid import ObjectId


class JobModel:
    def __init__(self, db):
        self.jobs = db['jobs']

    def add_job(self, company_name, job_title, job_number, job_description, link, mandatory_requirements=None,
                general_requirements=None, advantageous_requirements=None):
        if advantageous_requirements is None:
            advantageous_requirements = []
        if general_requirements is None:
            general_requirements = []
        if mandatory_requirements is None:
            mandatory_requirements = []
        job = {
            "company_name": company_name,
            "job_title": job_title,
            "job_number": job_number,
            "general_requirements": general_requirements,
            "mandatory_requirements": mandatory_requirements,
            "advantageous_requirements": advantageous_requirements,
            "job_description": job_description,
            "link_to_file": link
        }
        return self.jobs.insert_one(job).inserted_id

    def get_job(self, job_id):
        return self.jobs.find_one({"_id": ObjectId(job_id)})

    def get_job_by_number(self, job_number):
        return self.jobs.find_one({"job_number": job_number})

    def update_job(self, job_id, job_title, job_number, job_description):
        return self.jobs.update_one(
            {'_id': ObjectId(job_id)},
            {'$set': {'job_title': job_title, 'job_number': job_number, 'job_description': job_description}}
        )