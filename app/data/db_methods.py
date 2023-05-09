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
    def create_empty_document(col_ref: fs.CollectionReference):
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
    def fetch_doc(col_ref, document_name):
        doc = col_ref.document(f"{document_name}")
        return doc
    
    @staticmethod
    def fetch_doc_info(db, col_ref, document_name):
        doc = db.document(f"{col_ref}/{document_name}").get().to_dict()
        return doc

    @staticmethod
    def update_document_array_attribute(doc_ref, data: Dict[str, str]):
        field_name = list(data.keys())[0]
        data[field_name] = fs.ArrayUnion([data[field_name]])
        doc_ref.update(data)

    @staticmethod
    def remove_document_array_attribute(doc_ref, data: Dict[str, str]):
        field_name = list(data.keys())[0]
        data[field_name] = fs.ArrayRemove([data[field_name]])
        doc_ref.update(data)

    @staticmethod
    def update_document_non_array_attribute(doc_ref, data: Dict[str, str]):
        doc_ref.update(data)

    @staticmethod
    def remove_document_non_array_attribute(doc_ref, data: Dict[str, str]):
        field_name = list(data.keys())[0]
        data[field_name] = fs.DELETE_FIELD
        doc_ref.update(data)

    @staticmethod
    def check_if_property_exists_in_collection(db, collection_name: str, key: str, value: str) -> bool:
        docs = db.collection(collection_name).where(key, "==", value).get()
        if len(docs) > 0:
            return True
        else:
            docs = db.collection(collection_name).where(key, "array_contains", value).get()
            if len(docs) > 0:
                return True
            else:
                return False
            
    @staticmethod
    def check_if_properties_exist_in_collection(db, collection_name: str, properties: dict) -> bool:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.get()

        for doc in docs:
            doc_data = doc.to_dict()
            found_all_properties = True
            for key, value in properties.items():
                if key not in doc_data or value not in doc_data[key]:
                    found_all_properties = False
                    break
            if found_all_properties:
                return True
        
        return False
        
    @staticmethod
    def check_if_property_exists_in_document(db, collection_name: str, document_name: str, key: str, value: str) -> bool:
        doc = DataBaseMethods.check_if_document_exists_and_return_doc(db, collection_name, document_name)

        doc_data = doc.to_dict()

        if key not in doc_data:
            return False

        if value in doc_data[key]:
            return True
        else:
            return False
        
    @staticmethod
    def check_if_properties_exist_in_document(db, collection_name: str, document_name: str, properties: tuple) -> bool:
        doc = DataBaseMethods.check_if_document_exists_and_return_doc(db, collection_name, document_name)
        properties_found = []
        properties_not_found = []

        doc_data = doc.to_dict()

        for key, value in properties:
            if key not in doc_data or value not in doc_data[key]:
                properties_not_found.append(value)
            else:
                properties_found.append(value)

        return properties_found, properties_not_found
     
    @staticmethod
    def delete_document(doc_ref):
        try:
            response = doc_ref.delete()
            return response
        except Exception as e:
            print(f"Error deleting document: {e}")
            return None
        
    @staticmethod
    def check_if_document_exists_and_return_doc(db, collection_name: str, document_name: str):
        doc_ref = db.collection(collection_name).document(document_name)
        doc = doc_ref.get()

        if doc.exists:
            return doc
        else:
            raise Exception("Document does not exist")
