import unittest
import json
from app import create_app
from database.models import (
    Movie, 
    Actor, 
    db
)
from datetime import datetime

from settings import (
    DATABASE_URL_TEST,
    DATABASE_URL_TEST_LOCAL,
    CASTING_ASSISTANT_BEARER_TOKEN,
    CASTING_DIRECTOR_BEARER_TOKEN,
    EXECUTIVE_DIRECTOR_BEARER_TOKEN,
)


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = DATABASE_URL_TEST
        self.app = create_app(self.database_path)
        self.client = self.app.test_client()
        self.set_jwt_token()

        with self.app.app_context():
            db.create_all()
            Movie(title="The Shawshank Redemption", release_date="1994-09-01").insert()
            Movie(title="The Godfather", release_date="1972-12-15").insert()
            Movie(title="The Dark Knight", release_date="2008-12-10").insert()
            Movie(title="The Godfather Part II", release_date="1974-11-22").insert()
            Movie(title="12 Angry Men", release_date="1957-12-05").insert()

            first_movie = Movie.query.filter(
                Movie.title == "The Shawshank Redemption"
            ).first()
            if first_movie is not None:
                self.start_movie_id = first_movie.id

            Actor(name="Robert De Niro", age=81, gender="M").insert()
            Actor(name="Jack Nicholson", age=87, gender="M").insert()
            Actor(name="Marlon Brando", age=80, gender="M").insert()
            Actor(name="Denzel Washington", age=69, gender="M").insert()
            Actor(name="Katharine Hepburn", age=96, gender="F").insert()

            first_actor = Actor.query.filter(Actor.name == "Robert De Niro").first()
            if first_actor is not None:
                self.start_actor_id = first_actor.id

    def set_jwt_token(self):
        self.casting_assistant_jwt_token = CASTING_ASSISTANT_BEARER_TOKEN
        self.casting_director_jwt_token = CASTING_DIRECTOR_BEARER_TOKEN
        self.executive_director_jwt_token = EXECUTIVE_DIRECTOR_BEARER_TOKEN

    """GET movies test"""

    def test_get_movies_with_valid_url(self):
        """Test GET '/movies' with valid url"""
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        res = self.client.get("/movies", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["movies"])
        self.assertTrue(data["total_movies"])

    def test_get_movies_with_invalid_url(self):
        """Test GET '/movies' with invalid url"""
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        res = self.client.get("/movies/all", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    """GET actors test"""

    def test_get_actors_with_valid_url(self):
        """Test GET '/actors' with valid url"""
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        res = self.client.get("/actors", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["actors"])
        self.assertTrue(data["total_actors"])

    def test_get_actors_with_invalid_url(self):
        """Test GET '/actors' with invalid url"""
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        res = self.client.get("/actors/all", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    """GET /movies/<int:movie_id> test"""

    def test_get_movie_with_valid_url_and_id(self):
        """Test GET '/movies/<int:movie_id>' with valid url"""
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        res = self.client.get(f"/movies/{self.start_movie_id}", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["movie"])

    def test_get_movie_with_invalid_id(self):
        """Test GET '/movies/<int:movie_id>' with not existing movie id"""
        with self.app.app_context():
            movies = Movie.query.order_by(Movie.id).all()
            self.assertGreater(
                len(movies), 0, "No movies found in the database for test"
            )
            wrong_movie_id = movies[len(movies) - 1].id + 1

            headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
            res = self.client.get(f"/movies/{wrong_movie_id}", headers=headers)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "resource not found")

    """GET /actors/<int:actor_id> test"""

    def test_get_actor_with_valid_url_and_id(self):
        """Test GET '/actors/<int:actor_id>' with valid url"""
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        res = self.client.get(f"/actors/{self.start_actor_id}", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["actor"])

    def test_get_actor_with_invalid_id(self):
        """Test GET '/actors/<int:actor_id>' with not existing actor id"""
        with self.app.app_context():
            actors = Actor.query.order_by(Actor.id).all()
            self.assertGreater(
                len(actors), 0, "No actors found in the database for test"
            )
            wrong_actor_id = actors[len(actors) - 1].id + 1

            headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
            res = self.client.get(f"/movies/{wrong_actor_id}", headers=headers)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "resource not found")

    """DELETE /movies/<int:movie_id> test"""

    def test_delete_movie_with_valid_url_and_id(self):
        """Test DELETE '/movies/<int:movie_id>' with valid url"""
        with self.app.app_context():
            movies = Movie.query.order_by(Movie.id).all()
            self.assertGreater(
                len(movies), 0, "No movies found in the database to do the test"
            )
            headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
            res = self.client.delete(f"/movies/{self.start_movie_id}", headers=headers)
            movie_deleted = Movie.query.filter(
                Movie.id == self.start_movie_id
            ).one_or_none()
            self.assertIsNone(movie_deleted)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(data["deleted"])
            self.assertTrue(data["current_movies"])
            self.assertTrue(data["total_movies"])

    def test_delete_movie_with_valid_url_and_wrong_id(self):
        """Test DELETE '/movies/<int:movie_id>' with valid url and wrong id"""
        with self.app.app_context():
            movies = Movie.query.order_by(Movie.id).all()
            self.assertGreater(
                len(movies), 0, "No movies found in the database to do the test"
            )
            headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
            wrong_id = movies[len(movies) - 1].id + 1
            res = self.client.delete(f"/movies/{wrong_id}", headers=headers)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "resource not found")

    """DELETE /actors/<int:actor_id> test"""

    def test_delete_actor_with_valid_url_and_id(self):
        """Test DELETE '/actors/<int:actor_id>' with valid url"""
        with self.app.app_context():
            movies = Actor.query.order_by(Actor.id).all()
            self.assertGreater(
                len(movies), 0, "No actors found in the database to do the test"
            )
            headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
            res = self.client.delete(f"/actors/{self.start_movie_id}", headers=headers)
            actor_deleted = Actor.query.filter(
                Actor.id == self.start_actor_id
            ).one_or_none()
            self.assertIsNone(actor_deleted)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(data["deleted"])
            self.assertTrue(data["current_actors"])
            self.assertTrue(data["total_actors"])

    def test_delete_actor_with_valid_url_and_wrong_id(self):
        """Test DELETE '/actors/<int:actor_id>' with valid url and wrong id"""
        with self.app.app_context():
            actors = Actor.query.order_by(Actor.id).all()
            self.assertGreater(
                len(actors), 0, "No actors found in the database to do the test"
            )
            headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
            wrong_id = actors[len(actors) - 1].id + 1
            res = self.client.delete(f"/actors/{wrong_id}", headers=headers)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "resource not found")

    """POST '/movies' test"""

    def test_post_movies_good_weather(self):
        """Test POST '/movies' with valid data"""
        new_movie_data = {
            "title": "The Lord of the Rings: The Return of the King",
            "release_date": "2003-12-10",
        }
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        with self.app.app_context():
            res = self.client.post("/movies", json=new_movie_data, headers=headers)
            data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(data["created"])
            self.assertTrue(data["movies"])
            # Ensure total_movies count is correct
            self.assertEqual(data["total_movies"], len(Movie.query.all()))

    def test_post_movies_invalid_data(self):
        """Test POST '/movies' with invalid data"""
        new_movie_data = {}
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        with self.app.app_context():
            res = self.client.post("/movies", json=new_movie_data, headers=headers)
            data = res.get_json()
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "unprocessable")

    """POST '/actors' test"""

    def test_post_actors_good_weather(self):
        """Test POST '/actors' with valid data"""
        new_actor_data = {"name": "Anthony Hopkins", "age": "86", "gender": "M"}
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        with self.app.app_context():
            res = self.client.post("/actors", json=new_actor_data, headers=headers)
            data = res.get_json()
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(data["created"])
            self.assertTrue(data["actors"])
            # Ensure total_actors count is correct
            self.assertEqual(data["total_actors"], len(Actor.query.all()))

    def test_post_actors_invalid_data(self):
        """Test POST '/actors' with invalid data"""
        new_actor_data = {}
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        with self.app.app_context():
            res = self.client.post("/actors", json=new_actor_data, headers=headers)
            data = res.get_json()
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "unprocessable")

    """PATCH '/movies/<int:id>' test"""

    def test_patch_movies_good_weather(self):
        """Test PATCH '/movies/<int:id>' with valid data"""
        movie_name_to_patch = "The Shawshank Redemption"
        input_date = "1994-09-02"
        date_object = datetime.strptime(input_date, "%Y-%m-%d")
        formatted_date = date_object.strftime("%a, %d %b %Y 00:00:00 GMT")
        new_patch_data = {"release_date": formatted_date}
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        with self.app.app_context():
            movie_to_patch = Movie.query.filter(
                Movie.title == movie_name_to_patch
            ).one_or_none()
            res = self.client.patch(
                f"/movies/{movie_to_patch.id}", json=new_patch_data, headers=headers
            )
            data = res.get_json()
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(data["movie_patched"])
            # Ensure data patched is correct
            self.assertEqual(
                data["movie_patched"][0]["release_date"], new_patch_data["release_date"]
            )

    def test_patch_movies_invalid_data(self):
        """Test PATCH '/movies/<int:id>' with invalid data"""
        patch_movie_data = {}
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        movie_name_to_patch = "The Shawshank Redemption"
        with self.app.app_context():
            movie_to_patch = Movie.query.filter(
                Movie.title == movie_name_to_patch
            ).one_or_none()
            res = self.client.patch(
                f"/movies/{movie_to_patch.id}", json=patch_movie_data, headers=headers
            )
            data = res.get_json()
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "unprocessable")

    """PATCH '/actors' test"""

    def test_patch_actors_good_weather(self):
        """Test PATCH '/actors/<int:id>' with valid data"""
        actor_name_to_patch = "Robert De Niro"
        input_age = 82
        new_patch_data = {"age": input_age}
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        with self.app.app_context():
            actor_to_patch = Actor.query.filter(
                Actor.name == actor_name_to_patch
            ).one_or_none()
            res = self.client.patch(
                f"/actors/{actor_to_patch.id}", json=new_patch_data, headers=headers
            )
            data = res.get_json()
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(data["actor_patched"])
            # Ensure data patched is correct
            self.assertEqual(data["actor_patched"][0]["age"], new_patch_data["age"])

    def test_patch_actors_invalid_data(self):
        """Test PATCH '/actors/<int:id>' with invalid data"""
        patch_actor_data = {}
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        actor_name_to_patch = "Robert De Niro"
        with self.app.app_context():
            actor_to_patch = Actor.query.filter(
                Actor.name == actor_name_to_patch
            ).one_or_none()
            res = self.client.patch(
                f"/actors/{actor_to_patch.id}", json=patch_actor_data, headers=headers
            )
            data = res.get_json()
            self.assertEqual(res.status_code, 422)
            self.assertEqual(data["success"], False)
            self.assertEqual(data["message"], "unprocessable")

    """
     
    Test Role Base Access Control (RBAC)


    Test Casting Assistant RBAC:
        "permissions": [
        "get:actor",
        "get:actors",
        "get:movie",
        "get:movies"
    ] 

    Test RBAC good weather for Casting Assistant 
    """

    def test_get_movies_with_valid_url_with_jwt_casting_assistant(self):
        """Test GET '/movies' with valid url"""
        headers = {"Authorization": f"Bearer {self.casting_assistant_jwt_token}"}
        res = self.client.get("/movies", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["movies"])
        self.assertTrue(data["total_movies"])

    """Test RBAC bad weather for Casting Assistant"""

    def test_delete_movie_with_valid_url_and_id_with_jwt_casting_assistant(self):
        """Test DELETE '/movies/<int:movie_id>' with valid url"""
        with self.app.app_context():
            movies = Movie.query.order_by(Movie.id).all()
            self.assertGreater(
                len(movies), 0, "No movies found in the database to do the test"
            )
            headers = {"Authorization": f"Bearer {self.casting_assistant_jwt_token}"}
            res = self.client.delete(f"/movies/{self.start_movie_id}", headers=headers)
            movie_deleted = Movie.query.filter(
                Movie.id == self.start_movie_id
            ).one_or_none()
            self.assertIsNotNone(movie_deleted)
            self.assertEqual(res.status_code, 403)

    """ 
    Test Casting Director RBAC:
            "permissions": [
                "delete:actor",
                "get:actor",
                "get:actors",
                "get:movie",
                "get:movies",
                "patch:actor",
                "patch:movie",
                "post:actor"
            ]

    Test RBAC good weather for Casting Director 
    """

    def test_post_actors_good_weather_with_jwt_casting_director(self):
        """Test POST '/actors' with valid data"""
        new_actor_data = {"name": "Anthony Hopkins", "age": "86", "gender": "M"}
        headers = {"Authorization": f"Bearer {self.casting_director_jwt_token}"}
        with self.app.app_context():
            res = self.client.post("/actors", json=new_actor_data, headers=headers)
            data = res.get_json()
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(data["created"])
            self.assertTrue(data["actors"])
            # Ensure total_actors count is correct
            self.assertEqual(data["total_actors"], len(Actor.query.all()))

    """Test RBAC bad weather for Casting Director"""

    def test_delete_movie_with_valid_url_and_id_with_jwt_casting_director(self):
        """Test DELETE '/movies/<int:movie_id>' with valid url"""
        with self.app.app_context():
            movies = Movie.query.order_by(Movie.id).all()
            self.assertGreater(
                len(movies), 0, "No movies found in the database to do the test"
            )
            headers = {"Authorization": f"Bearer {self.casting_director_jwt_token}"}
            res = self.client.delete(f"/movies/{self.start_movie_id}", headers=headers)
            movie_deleted = Movie.query.filter(
                Movie.id == self.start_movie_id
            ).one_or_none()
            self.assertIsNotNone(movie_deleted)
            self.assertEqual(res.status_code, 403)

    """ 
    Test Executive Director RBAC:
            "permissions": [
            "delete:actor",
            "delete:movie",
            "get:actor",
            "get:actors",
            "get:movie",
            "get:movies",
            "patch:actor",
            "patch:movie",
            "post:actor",
            "post:movie"
        ]

    Test RBAC good weather for Executive Director 
    """

    def test_delete_actor_with_valid_url_and_id_with_jwt_executive_director(self):
        """Test DELETE '/actors/<int:actor_id>' with valid url"""
        with self.app.app_context():
            movies = Actor.query.order_by(Actor.id).all()
            self.assertGreater(
                len(movies), 0, "No actors found in the database to do the test"
            )
            headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
            res = self.client.delete(f"/actors/{self.start_movie_id}", headers=headers)
            actor_deleted = Actor.query.filter(
                Actor.id == self.start_actor_id
            ).one_or_none()
            self.assertIsNone(actor_deleted)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(data["deleted"])
            self.assertTrue(data["current_actors"])
            self.assertTrue(data["total_actors"])

    """Test RBAC good weather for Executive Director"""

    def test_post_movies_good_weather_with_jwt_executive_director(self):
        """Test POST '/movies' with valid data"""
        new_movie_data = {
            "title": "The Lord of the Rings: The Return of the King",
            "release_date": "2003-12-10",
        }
        headers = {"Authorization": f"Bearer {self.executive_director_jwt_token}"}
        with self.app.app_context():
            res = self.client.post("/movies", json=new_movie_data, headers=headers)
            data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["success"])
            self.assertTrue(data["created"])
            self.assertTrue(data["movies"])
            # Ensure total_movies count is correct
            self.assertEqual(data["total_movies"], len(Movie.query.all()))

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
