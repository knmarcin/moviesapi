from rest_framework.test import APITestCase
from utils.connector import APIConnector, MovieClass

class TestConnector(APITestCase):
    """Testing simple scenario if it gets data"""
    def setUp(self) -> None:
        self.q='Hobbit'
        c = APIConnector(self.q)
        self.created = c.get_movie_data()

    def test_if_gets_data(self):
        self.assertEqual(self.created, 201)

class TestConnectorBadRequest(APITestCase):
    """Testing handling error if resource wasn't found in external API"""
    def setUp(self) -> None:
        self.q = 'wrog u bram'
        c = APIConnector(self.q)
        self.created = c.get_movie_data()

    def test_if_created(self):
        self.q = 'wrog u bram'
        self.assertEqual(self.created, 404)


