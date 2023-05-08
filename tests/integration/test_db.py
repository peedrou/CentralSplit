import random
from dotenv import load_dotenv
from google.cloud import firestore as fs
from app.data.db_methods import DataBaseMethods as DBM

load_dotenv()

class TestDatabaseAccessIntegration():

    def _make_random_name(self) -> str:
        my_string = "abcdefghijklmnopqrstuvwxyz"
        random_string = ''.join(random.choices(my_string, k=10))
        return random_string

    def test_db_access(self):
        db = DBM.get_db()

        assert isinstance(db, fs.Client)

    def test_get_collection(self):
        db = DBM.get_db()
        col_ref = DBM.get_collection(db, "Groups")

        assert isinstance(col_ref, fs.CollectionReference)

    def test_create_empty_document_and_add_info(self):
        db = DBM.get_db()
        col_ref = DBM.get_collection(db, "TestCollection")
        empty_doc = DBM.create_empty_document(col_ref)
        doc_ref = DBM.add_new_info_to_document(empty_doc, {})

        assert doc_ref is not None

    def test_create_document_with_title(self):
        random_name = self._make_random_name()
        info = {'test_key':'test value'}

        db = DBM.get_db()
        col_ref = DBM.get_collection(db, "TestCollection")
        doc = DBM.create_document_with_title(col_ref, random_name)
        DBM.add_new_info_to_document(doc, info)
        doc_data = DBM.fetch_doc_info(db, "TestCollection", random_name)

        assert isinstance(doc, fs.DocumentReference)
        assert doc_data['test_key'] == 'test value'

    def test_fetch_doc_ID(self):
        random_name = self._make_random_name()

        db = DBM.get_db()
        col_ref = DBM.get_collection(db, "TestCollection")
        doc = DBM.create_document_with_title(col_ref, random_name)
        doc_id = DBM.fetch_doc_id(doc),

        assert doc_id[0] == random_name

    def test_delete_doc(self):
        random_name = self._make_random_name()
        info = {'test_key':'test value'}

        db = DBM.get_db()
        col_ref = DBM.get_collection(db, "TestCollection")
        doc_creation = DBM.create_document_with_title(col_ref, random_name)
        DBM.add_new_info_to_document(doc_creation, info)
        doc = DBM.fetch_doc(col_ref, random_name)
        deleted_doc = DBM.delete_document(doc)

        assert deleted_doc is not None

    def test_update_document_attribute(self):
        random_name = self._make_random_name()
        info = {'test_key':'test value'}

        db = DBM.get_db()
        col_ref = DBM.get_collection(db, "TestCollection")
        doc_creation = DBM.create_document_with_title(col_ref, random_name)
        DBM.add_new_info_to_document(doc_creation, info)
        doc = DBM.fetch_doc(col_ref, random_name)
        DBM.update_document_attribute(doc, {'test_key':'new value'})

        doc_with_new_info = DBM.fetch_doc_info(db, "TestCollection", random_name)
        
        assert doc_with_new_info["test_key"] == "new value"

    def test_if_list_property_exists_in_document(self):
        db = DBM.get_db()
        response = DBM.check_if_property_exists_in_document(db, "Groups", "Test Group 2", "members", "user2")

        assert response == True

    def test_if_non_list_property_exists_in_document(self):
        db = DBM.get_db()
        response = DBM.check_if_property_exists_in_document(db, "Groups", "Test Group 2", "groupName", "Test Group 2")

        assert response == True

    def test_if_properties_exist_in_document(self):
        db = DBM.get_db()
        properties = [ ('members', 'user1'), ('members', 'user2'), ('members', 'user3')]
        properties_found, properties_not_found = DBM.check_if_properties_exist_in_document(db, "Groups", "Test Group 2", properties)

        assert properties_found == ['user1','user2','user3']
        assert properties_not_found == []

    def test_if_property_exists_in_collection(self):
        db = DBM.get_db()
        response = DBM.check_if_property_exists_in_collection(db, "Groups", "groupName", "Test Group 2")

        assert response == True

    def test_if_properties_exist_in_collection(self):
        db = DBM.get_db()
        properties = {
            'members':'user1',
            'members':'user2',
            'members':'user3',
        }
        response = DBM.check_if_properties_exist_in_collection(db, "Groups", properties)

        assert response == True