from dotenv import load_dotenv
from google.cloud import firestore as fs
from app.data.db_methods import DataBaseMethods as DBM

load_dotenv()

class TestDatabaseAccessIntegration():

    def test_db_access(self):
        db = DBM.get_db()
        assert isinstance(db, fs.Client)

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
        properties = {
            'members':'user1',
            'members':'user2',
            'members':'user3',
        }
        response = DBM.check_if_properties_exist_in_document(db, "Groups", "Test Group 2", properties)
        assert response == True