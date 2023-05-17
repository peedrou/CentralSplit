import os
from dotenv import load_dotenv
from google.cloud import firestore as fs
from typing import Dict, List, Any

load_dotenv()

class DataBaseMethods():

    @staticmethod
    def get_db() -> fs.Client:
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        db = fs.Client.from_service_account_json(credentials_path)
        return db
    
    @staticmethod
    def get_collection(db, collection_name: str) -> Any:
        col_ref = db.collection(f"{collection_name}")
        return col_ref
    
    @staticmethod
    def create_empty_document(col_ref: fs.CollectionReference) -> fs.DocumentReference:
        doc_ref = col_ref.document()
        return doc_ref
    
    @staticmethod
    def create_document_with_title(col_ref: fs.CollectionReference, title: str) -> fs.DocumentReference:
        doc_ref = col_ref.document(title)
        return doc_ref
    
    @staticmethod
    def add_new_info_to_document(doc_ref, data: Dict[str, any]) -> Any:
        try:
            response = doc_ref.set(data)
            return response
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def fetch_doc_id(doc_ref) -> Any:
        doc_id = doc_ref.id
        return doc_id
    
    @staticmethod
    def fetch_doc(col_ref, document_name) -> Any:
        doc = col_ref.document(f"{document_name}")
        return doc
    
    @staticmethod
    def fetch_doc_info(db, col_ref, document_name) -> Dict[str, Any]:
        doc = db.document(f"{col_ref}/{document_name}").get().to_dict()
        return doc

    @staticmethod
    def update_document_array_attribute(doc_ref, data: Dict[str, str]) -> None:
        field_name = list(data.keys())[0]
        data[field_name] = fs.ArrayUnion([data[field_name]])
        try:
            doc_ref.update(data)
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def remove_document_array_attribute(doc_ref, data: Dict[str, str]) -> None:
        field_name = list(data.keys())[0]
        data[field_name] = fs.ArrayRemove([data[field_name]])
        doc_ref.update(data)

    @staticmethod
    def update_document_non_array_attribute(doc_ref, data: Dict[str, any]) -> None:
        try:
            doc_ref.update(data)
        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def remove_document_non_array_attribute(doc_ref, data: Dict[str, str]) -> None:
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
    def check_if_property_exists_in_collection_and_return_doc(db, collection_name: str, key: str, value: str) -> List[fs.DocumentReference]:
        docs = db.collection(collection_name).where(key, "==", value).get() 
        doc_list = []
        if len(docs) > 0:
            for doc in docs:
                doc_ref = doc.reference
                doc_list.append(doc_ref)
            return doc_list
        else:
            docs = db.collection(collection_name).where(key, "array_contains", value).get()
            if len(docs) > 0:
                for doc in docs:
                    doc_ref = doc.reference
                    doc_list.append(doc_ref)
                    return doc_list
            else:
                return None

            
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
    def check_if_property_exists_in_document_with_doc_ref(doc_ref, key: str, value: str) -> bool:
        if doc_ref is dict:
            doc_data = doc_ref.to_dict()
        else:
            doc_data = doc_ref

        if key not in doc_data:
            return False

        if value in doc_data[key]:
            return True
        else:
            return False
        
    @staticmethod
    def check_if_property_exists_in_document_with_doc_ref_and_return_value(doc_ref, key: str) -> Any:
        doc_data = doc_ref.get().to_dict()

        if key not in doc_data:
            return False
        else:
            return doc_data[key]
        
    @staticmethod
    def check_if_properties_exist_in_document(db, collection_name: str, document_name: str, properties: tuple) -> List[Any]:
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
    def delete_document(doc_ref) -> Any:
        try:
            response = doc_ref.delete()
            return response
        except Exception as e:
            print(f"Error deleting document: {e}")
            return None
        
    @staticmethod
    def check_if_document_exists_and_return_doc(db, collection_name: str, document_name: str) -> fs.DocumentSnapshot:
        doc_ref = db.collection(collection_name).document(document_name)
        doc = doc_ref.get()

        if doc.exists:
            return doc
        else:
            raise Exception("Document does not exist")
