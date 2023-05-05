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
        col_ref = db.collection(f"{collection_name}")
        return col_ref
    
    @staticmethod
    def create_empty_document(col_ref):
        doc_ref = col_ref.document()
        return doc_ref
    
    @staticmethod
    def create_document_with_title(col_ref: fs.CollectionReference, title: str):
        doc_ref = col_ref.document(title)
        return doc_ref
    
    @staticmethod
    def add_new_info_to_document(doc_ref, data: Dict[str, any]):
        response = doc_ref.set(data)
        return response

    @staticmethod
    def fetch_doc_id(doc_ref):
        doc_id = doc_ref.id
        return doc_id
    
    @staticmethod
    def fetch_doc(db, col_ref, document_name):
        doc = db.document(f"{col_ref}/{document_name}").get().to_dict()
        return doc

    @staticmethod
    def update_document_attribute(doc_ref, data: Dict[str, str]):
        doc_ref.update(data)

    @staticmethod
    def check_if_property_exists(db, collection_name: str, key: str, value: str) -> bool:
        docs = db.collection(collection_name).where(key, "==", value).get()
        if len(docs) > 0:
            return True
        else:
            return False
