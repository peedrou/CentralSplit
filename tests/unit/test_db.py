import os
from dotenv import load_dotenv

load_dotenv()

class TestDatabaseAccessUnit():

    def test_API_key(self):
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        assert credentials_path is not None
