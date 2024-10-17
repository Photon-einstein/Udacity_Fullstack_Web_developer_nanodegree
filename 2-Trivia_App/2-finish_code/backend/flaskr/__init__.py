import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(db_URI="", test_config=None):
    app = Flask(__name__)
    if db_URI:
        setup_db(app, db_URI)
    else:
        setup_db(app)

    """
    @TODO DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin",
                             "*")  # Allow all origins
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=['GET'])
    def get_categories():
        try:
            categories_bulk = Category.query.order_by(Category.id).all()
            if len(categories_bulk) == 0:
                abort(404)
            categories = {}
            for entry in categories_bulk:
                categories.update({entry.id: entry.type})
            return jsonify(
                {
                    "success": True,
                    "categories": categories,
                    "total_categories": len(categories),
                }
            )
        except ValueError:
            # Handle specific error for invalid data types
            abort(404)

    """
    @TODO DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @app.route("/questions", methods=['GET'])
    def retrieve_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            if len(current_questions) == 0:
                abort(404)
            categories = Category.query.order_by(Category.id).all()
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                    "current_category": None,
                    "categories": {category.id: category.type for category in categories}
                }
            )
        except ValueError:
            # Handle specific error for invalid data types
            abort(404)

    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(422)

    """
    @TODO DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions", methods=["POST"])
    def create_questions():
        body = request.get_json()
        search = body.get("search_term", None)
        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search)))
                current_questions = paginate_questions(request, selection)
                if len(current_questions) == 0:
                    abort(404)
                categories = Category.query.order_by(Category.id).all()
                categories_formatted = [category.format()
                                        for category in categories]
                return jsonify(
                    {
                        "success": True,
                        "created": None,
                        "questions": current_questions,
                        "total_questions": len(current_questions),
                        "current categories": categories_formatted
                    }
                )
            else:
                new_question = body.get("question", None)
                new_answer = body.get("answer", None)
                new_category = body.get("category", None)
                new_difficulty = body.get("difficulty", None)

                if not new_question or not new_answer or not new_category or not new_difficulty:
                    abort(422)
                question = Question(question=new_question,
                                    answer=new_answer,
                                    category=new_category,
                                    difficulty=new_difficulty)
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)
                categories = Category.query.order_by(Category.id).all()
                categories_ids = [category.id for category in categories]

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                        "categories_ids": categories_ids
                    }
                )
        except:
            abort(422)

    """
    @TODO DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/categories/<int:category>/questions", methods=['GET'])
    def retrieve_questions_by_category(category):
        try:
            selection = Question.query.filter(
                Question.category == category).order_by(Question.id)
            current_questions_by_category = paginate_questions(
                request, selection)
            if len(current_questions_by_category) == 0:
                abort(404)
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions_by_category,
                    "total_questions": len(current_questions_by_category),
                    "current_category": category
                }
            )
        except ValueError:
            # Handle specific error for invalid data types
            abort(404)
    """
    @TODO DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def play_questions():
        body = request.get_json()
        if not body:
            abort(400)
        try:
            previous_questions = body.get("previous_questions", None)
            quiz_category = body.get("quiz_category", None)
            if previous_questions is None:
                if quiz_category:
                    questions_raw = Question.query.filter(
                        Question.category == str(quiz_category['id'])).order_by(Question.id)
                else:
                    questions_raw = Question.query.order_by(Question.id).all()
            else:
                quiz_type = quiz_category.get('type', None)
                categories = Category.query.order_by(Category.id).all()
                category_code_max = categories[-1].id + 1
                if quiz_type and quiz_type != 'click':
                    questions_raw = Question.query.filter(Question.category == str(quiz_category['id'])).filter(
                        Question.id.notin_(previous_questions)).order_by(Question.id)
                elif quiz_category['id'] < category_code_max:
                    questions_raw = Question.query.filter(
                        Question.id.notin_(previous_questions)).order_by(Question.id)
                else:
                    abort(422)

            questions_paginated_to_choose_from = paginate_questions(
                request, questions_raw)

            # If no more questions are available, return a signal to end the quiz
            if len(questions_paginated_to_choose_from) == 0:
                return jsonify({
                    "success": True,
                    "question": None
                })

            if questions_paginated_to_choose_from:
                question_choosen = questions_paginated_to_choose_from[random.randint(
                    0, len(questions_paginated_to_choose_from)-1)]
                return jsonify(
                    {
                        "success": True,
                        "question": question_choosen
                    }
                )
            else:
                abort(404)
        except Exception as e:
            abort(422)

    """
    @TODO DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500,
                    "message": "internal server error"}),
            500,
        )

    return app
