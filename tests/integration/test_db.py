import os
from dotenv import load_dotenv
from google.cloud import firestore as fs

load_dotenv()

class TestDatabaseAccessIntegration():

    def test_db_access(self):
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        db = fs.Client.from_service_account_json(credentials_path)
        doc_ref = db.collection("new collection").document()
        doc_ref.set({
            "name": "John Doe",
            "email": "johndoe@example.com"
        })
        bruh = 1 + 1
        assert bruh == 2