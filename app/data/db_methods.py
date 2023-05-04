import os
from dotenv import load_dotenv
from google.cloud import firestore as fs
from typing import Dict

load_dotenv()

class DataBaseMethods():

    @staticmethod
    def get_db():
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        db = fs.Client.from_service_account_json(credentials_path)
        return db
    
    @staticmethod
    def get_collection(db, collection_name: str):
        doc_ref = db.collection(f"{collection_name}").document()
        return doc_ref
    
    @staticmethod
    def add_to_collection(doc_ref, data: Dict[str, str]):
        pass
