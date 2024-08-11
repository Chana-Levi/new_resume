class OrganizationModel:
    def __init__(self, db):
        self.organizations = db['organizations']

    def add_organization(self, email, name):
        organization = {
            "email": email,
            "name": name,
        }
        return self.organizations.insert_one(organization).inserted_id

    def get_organization_by_email(self, email):
        return self.organizations.find_one({"email": email})