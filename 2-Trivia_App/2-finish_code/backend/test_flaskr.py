import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from settings import DB_TEST_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    deleted_question = {}

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = DB_TEST_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, "localhost:5432", self.database_name
        )
        self.app = create_app(self.database_path)
        self.client = self.app.test_client()

    """GET categories test"""

    def test_get_categories_with_valid_url(self):
        """Test GET '/categories' with valid url"""
        res = self.client.get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    def test_get_categories_with_invalid_url(self):
        """Test GET '/categories' with invalid url"""
        res = self.client.get("/categories/4")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    """GET questions test"""

    def test_get_with_questions_with_valid_url(self):
        """Test GET '/questions' with valid url"""
        res = self.client.get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['categories'])

    def test_get_questions_with_invalid_url(self):
        """Test GET '/questions' with page too high"""
        res = self.client.get(f"/questions/page=3")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    """DELETE questions test"""

    def test_delete_question_with_right_id(self):
        """Test delete 'question/<int:question_id>' with right id"""
        with self.app.app_context():
            questions = Question.query.order_by(Question.id).all()
            self.assertGreater(
                len(questions), 0, "No questions found in the database for testing")
            right_id = str(questions[0].id)
            self.deleted_question = {
                "question": questions[0].question,
                "answer": questions[0].answer,
                "category": questions[0].category,
                "difficulty": questions[0].difficulty
            }
            res = self.client.delete(f"/questions/{right_id}")
            self.assertEqual(res.status_code, 200)
            question = Question.query.filter(
                Question.id == right_id).one_or_none()
            self.assertIsNone(question)
            data = json.loads(res.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['deleted'], int(right_id))

    def test_delete_question_with_wrong_id(self):
        """Test delete 'questions/<int:question_id>' with wrong id"""
        with self.app.app_context():
            questions = Question.query.order_by(Question.id).all()
            self.assertGreater(
                len(questions), 0, "No questions found in the database for testing")
            wrong_id = str(questions[0].id-1)
            res = self.client.delete(f"/questions/{wrong_id}")
            self.assertEqual(res.status_code, 422)
            data = json.loads(res.data)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], "unprocessable")

    """POST creation questions test"""

    def test_create_question_good_weather(self):
        """Test POST '/questions' with valid data"""
        new_question_data = {
            "question": "What is the capital city of Mongolia?",
            "answer": "Ulaanbaatar",
            "category": 3,
            "difficulty": 5
        }
        with self.app.app_context():
            res = self.client.post("/questions", json=new_question_data)
            data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['created'])
            self.assertTrue(data['questions'])
            # Ensure total_questions count is correct
            self.assertEqual(data['total_questions'],
                             len(Question.query.all()))

    def test_create_question_bad_weather(self):
        """Test POST '/questions' with invalid data"""
        new_question_data = {}
        with self.app.app_context():
            res = self.client.post("/questions", json=new_question_data)
            data = res.get_json()

            self.assertEqual(res.status_code, 422)
            data = json.loads(res.data)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], "unprocessable")

    """POST search questions test"""

    def test_search_question_using_substring_good_weather(self):
        """Test POST '/questions' to search an existing question using a substring, good weather scenario"""
        new_question_search_term = {"search_term": "title", }
        with self.app.app_context():
            res = self.client.post("/questions", json=new_question_search_term)
            data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['questions'])
            self.assertTrue(data['total_questions'])

    def test_search_question_using_substring_bad_weather(self):
        """Test POST '/questions' to search an existing question using a substring, bad weather scenario"""
        new_question_search_term = {"search_term": "oops"}
        with self.app.app_context():
            res = self.client.post("/questions", json=new_question_search_term)
            data = res.get_json()

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], "unprocessable")

    """GET question based on category test"""

    def test_search_question_by_category_good_weather(self):
        """Test GET '/categories/<int:category>/questions', good weather scenario"""
        science_category_code = 1
        with self.app.app_context():
            res = self.client.get(
                f"/categories/{science_category_code}/questions")
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['questions'])
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['current_category'])

    def test_search_question_by_category_bad_weather(self):
        """Test GET '/categories/<int:category>/questions', bad weather scenario"""
        with self.app.app_context():
            categories = Category.query.order_by(Category.id).all()
            category_code_not_existing = categories[-1].id + 1

            res = self.client.get(
                f"/categories/{category_code_not_existing}/questions")
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], "resource not found")

    """POST for quizzes game """

    def test_post_for_quizzes_game_good_weather(self):
        """Test POST '/quizzes', good weather scenario"""
        quizz_data = {"previous_questions": [1, 2, 3],
                      "quiz_category": {"id": 1}
                      }
        with self.app.app_context():
            res = self.client.post("/quizzes", json=quizz_data)
            data = res.get_json()

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['question'])

    def test_post_for_quizzes_game_bad_weather(self):
        """Test POST '/quizzes', bad weather scenario"""
        with self.app.app_context():
            categories = Category.query.order_by(Category.id).all()
            category_code_not_existing = categories[-1].id + 1

            quizz_data = {"previous_questions": [1, 2, 3],
                          "quiz_category": {"id": category_code_not_existing}
                          }

            res = self.client.post("/quizzes", json=quizz_data)
            data = res.get_json()

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], "unprocessable")

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            # Delete new question introduced during this test
            questions = Question.query.all()
            for question in questions:
                if question.question == "What is the capital city of Mongolia?":
                    question.delete()
            # Reestablish deleted entry
            res = self.client.post("/questions", json=self.deleted_question)

if __name__ == "__main__":
    unittest.main()
