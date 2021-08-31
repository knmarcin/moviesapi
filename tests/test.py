from rest_framework.test import APITestCase

from movies.models import Movie


class MoviesApiResponseTest(APITestCase):
    def test_movies_response(self):
        """ Simple get test. First should be 204, because of empty database """
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 204)

    def test_post_data(self):
        """ Simple post test, should be 201, because of created"""
        response = self.client.post(
            "/movies/",
            {
                "question": "hobbit"
            }
        )

        self.assertEqual(response.status_code, 201)

    def test_get_after_post(self):
        """ Test on get on non empty db"""
        response = self.client.post(
            "/movies/",
            {
                "question": "hobbit"
            }
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 200)


    def test_post_no_data_in_external_api(self):
        """ Test on response on data which is not in external API"""
        response = self.client.post(

            "/movies/",
            {
                "question": "wrog u bram"
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_post_get_or_create(self):
        """ Test on doubled data, second code shouldn't be same as the first one"""
        response = self.client.post(
            "/movies/",
            {
                "question": "hobbit"
            }
        )

        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            "/movies/",
            {
                "question": "hobbit"
            }
        )
        self. assertEqual(response.status_code, 204)

    def test_get_correct_filters(self):
        """ Filter tests, checks if you can use many arguments in one filter"""
        self.client.post(
            "/movies/",
            {
                "question": "Unexpected Journey"
            }
        )

        self.client.post(
            "/movies/",
            {
                "question": "Desolation of Smaug"
            }
        )

        self.client.post(
            "/movies/",
            {
                "question": "The Battle of the Five Armies"
            }
        )

        response = self.client.get('/movies/', {'Director': 'Peter Jackson'})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/movies/', {'Director': ['Jackson', 'Peter']})
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/movies/', {'Director': ['Jackson', 'Michael', 'Peter']})
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/movies/', {'Director': 'Nolan Christopher'})
        self.assertEqual(response.status_code, 204)

        response = self.client.get('/movies/', {'Rated': 'PG-13'})
        self.assertEqual(response.status_code, 200)

    def test_get_sort(self):
        self.client.post(
            "/movies/",
            {
                "question": "Unexpected Journey"
            }
        )
        self.client.post(
            "/movies/",
            {
                "question": "The Battle of the Five Armies"
            }
        )


        self.client.post(
            "/movies/",
            {
                "question": "Desolation of Smaug"
            }
        )

        # Simple test if two same objects
        A = Movie.objects.all()
        B = Movie.objects.all()
        A = A.first()
        B = B.first()
        self.assertEqual(A,B)

        # test if default sorting works
        A = Movie.objects.all()
        B = Movie.objects.all()
        A = A.first()
        B = B.order_by('id').first()
        self.assertEqual(A,B)

        # test if sorting works desc
        A = Movie.objects.all()
        B = Movie.objects.all()
        A = A.first()
        B = B.order_by('-Data__Year').first()
        self.assertEqual(A,B)

        # test if sorting works asc
        A = Movie.objects.all()
        B = Movie.objects.all()
        A = A.first()
        B = B.order_by('Data__Year').first()
        self.assertNotEqual(A,B)



