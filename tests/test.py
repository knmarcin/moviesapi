from rest_framework.test import APITestCase

from movies.models import Movie


# Movie
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


class TestFilters(APITestCase):
    """ Filter tests, checks if you can use many arguments in one filter"""
    def setUp(self) -> None:
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

    def test_easiest_case(self):
        response = self.client.get('/movies/', {'Director': 'Peter Jackson'})
        self.assertEqual(response.status_code, 200)

    def test_filter_two_arguments_one_key(self):
        response = self.client.get('/movies/', {'Director': ['Jackson', 'Peter']})
        self.assertEqual(response.status_code, 200)

    def test_filter_three_arguments_one_key(self):
        response = self.client.get('/movies/', {'Director': ['Jackson', 'Michael', 'Peter']})
        self.assertEqual(response.status_code, 204)

    def test_empty_response(self):
        response = self.client.get('/movies/', {'Director': 'Nolan Christopher'})
        self.assertEqual(response.status_code, 204)

    def test_filter_different_arg(self):
        response = self.client.get('/movies/', {'Rated': 'PG-13'})
        self.assertEqual(response.status_code, 200)


class TestSort(APITestCase):
    def setUp(self) -> None:
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

    def test_same_objects(self):
        a = Movie.objects.all()
        b = Movie.objects.all()
        a = a.first()
        b = b.first()
        self.assertEqual(a, b)

        # test if default sorting works
    def test_default_sorting(self):
        a = Movie.objects.all()
        b = Movie.objects.all()
        a = a.first()
        b = b.order_by('id').first()
        self.assertEqual(a, b)

        # test if sorting works desc
    def test_sorting_desc(self):
        a = Movie.objects.all()
        b = Movie.objects.all()
        a = a.first()
        b = b.order_by('-Data__Year').first()
        self.assertEqual(a, b)

        # test if sorting works asc
    def test_sorting_asc(self):
        a = Movie.objects.all()
        b = Movie.objects.all()
        a = a.first()
        b = b.order_by('Data__Year').first()
        self.assertNotEqual(a, b)


# Comments
class TestCommentsResponse(APITestCase):
    def test_empty_list_response(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, 204)

    def test_post_response_id_does_not_exist(self):
        response = self.client.post(
            "/comments/",
            {
                "comment": "That is fantastic movie!",
                "movie_id": 3
            }
        )
        self.assertEqual(response.status_code, 400)


class TestComments(APITestCase):
    def setUp(self) -> None:
        self.movie = Movie.objects.create(id=1, Data={"Year": 2011})

    def test_comments_response(self):
        response = self.client.get("/comments/")
        self.assertEqual(response.status_code, 204)

    def test_post_responses(self):
        response = self.client.post(
            '/comments/',
            {
                'comment': 'That is fantastic movie!',
                'movie_id': 1
            }
        )
        self.assertEqual(response.status_code, 201)


class TestFilterComments(APITestCase):
    def setUp(self) -> None:
        Movie.objects.create(id=1, Data={"Year": 2011})
        Movie.objects.create(id=2, Data={"Year": 2012})
        Movie.objects.create(id=3, Data={"Year": 2013})

        self.client.post(
            '/comments/',
            {
                'comment': 'That is fantastic movie!',
                'movie_id': 1
            }
        )
        self.client.post(
            '/comments/',
            {
                'comment': 'Outstanding!',
                'movie_id': 1
            }
        )

    def test_comment_filter(self):
        response = self.client.get('/comments/', {'id': 1})
        self.assertEqual(response.status_code, 200)

    def test_comment_filter_empty_response(self):
        response = self.client.get('/comments/', {'id': 6})
        self.assertEqual(response.status_code, 204)
