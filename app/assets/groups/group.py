from dataclasses import dataclass
from typing import List

from app.data.db_methods import DataBaseMethods as DBM
from dotenv import load_dotenv

from app.support.abstracts.group import AbstractGroup

load_dotenv()

@dataclass
class Group(AbstractGroup):
    groupName: str
    members: List[str] | None

    def handle_create_group(self):
        groupName, db, check_group = self.get_group_query("groupName")

        if check_group == True:
            raise Exception("Group already exists with that name, please insert a different name")
        else:
            try:
                group_collection = DBM.get_collection(db, "Groups")
                doc_ref = DBM.create_document_with_title(group_collection, groupName)
                group_info = {
                    "groupName":f"{groupName}",
                    "members":self.members,
                }
                DBM.add_new_info_to_document(doc_ref, group_info)
                print(f"Group was created with Name: {groupName}")
                new_group = DBM.fetch_doc_info(db, "Groups", groupName)
                return new_group
            except Exception as e:
                raise Exception(e)

    
    def handle_delete_group(self):
        groupName, db, check_group = self.get_group_query("groupName")

        if check_group == True:
            try:
                group_collection = DBM.get_collection(db, "Groups")
                doc_ref = DBM.fetch_doc(group_collection, groupName)
                response = DBM.delete_document(doc_ref)
                return response
            except:
                raise Exception("Group could not be deleted")
        else:
            raise Exception("Group does not exist")

    def handle_add_users_to_group(self):
        groupName, db, check_group = self.get_group_query("groupName")

        if check_group == True:
            try:
                pass
                # group_collection = DBM.get_collection(db, "Groups")
                # doc_ref = DBM.fetch_doc(group_collection, groupName)
                # check_users
                
                # return response
            except:
                raise Exception("User/s could not be added")
        else:
            raise Exception("Group does not exist")

    def handle_remove_users_from_group(self):
        pass

    def get_group_query(self, property: str):
        groupName = self.groupName

        db = DBM.get_db()
        check_group = DBM.check_if_property_exists_in_collection(db, "Groups", property, groupName)
        return groupName,db,check_group
    
    def check_if_users_exists_in_group(self, users: List[str]):
        groupName = self.groupName

        db = DBM.get_db()
        check_user = DBM.check_if_property_exists(db, "Groups", property, groupName)
        return groupName
