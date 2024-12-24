from dotenv import load_dotenv
import os
from flask import (
    Flask, 
    request, 
    jsonify, 
    abort
)
from sqlalchemy import (
    exc, 
    text
)
import json
from flask_cors import CORS
from flask import redirect

from database.models import (
    setup_db, 
    Movie, 
    Actor, 
    db
)
from auth.auth import (
    AuthError, 
    requires_auth
)
from settings import (
    AUTH0_DOMAIN,
    API_AUDIENCE,
    CLIENT_ID,
    AUTH0_CALLBACK_URL_LOCAL,  # choose one of this two values
    AUTH0_CALLBACK_URL,
    DATABASE_URL_TEST_LOCAL,
    DATABASE_URL_LOCAL,  # choose one of this two values
    DATABASE_URL_PRODUCTION,
)


def create_app(database_path, test_config=None):
    app = Flask(__name__)
    setup_db(app, database_path)
    """
    Root endpoint
    """

    @app.route("/", methods=["GET"])
    def root():
        auth0_domain = AUTH0_DOMAIN
        api_audience = API_AUDIENCE
        client_id = CLIENT_ID
        auth0_callback_url = AUTH0_CALLBACK_URL

        url = "https://"
        url += f"{auth0_domain}"
        url += "/authorize?"
        url += f"audience={api_audience}&"
        url += "response_type=token&"
        url += f"client_id={client_id}&"
        url += f"redirect_uri={auth0_callback_url}"
        return redirect(url)

    @app.route("/success", methods=["GET"])
    def login():
        msg = "Login successful"
        return jsonify(msg)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")  # Allow all origins
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    Endpoint to handle GET requests
    for all available movies.
    """

    @app.route("/movies", methods=["GET"])
    @requires_auth("get:movies")
    def get_movies(jwt):
        try:
            movies_bulk = Movie.query.order_by(Movie.id).all()
            if len(movies_bulk) == 0:
                abort(404)
            movies_formatted = [movie.format() for movie in movies_bulk]
            return jsonify(
                {
                    "success": True,
                    "movies": movies_formatted,
                    "total_movies": len(movies_formatted),
                }
            )
        except ValueError:
            # Handle specific error for invalid data types
            abort(404)

    """
    Endpoint to handle GET requests
    for all available Actors.
    """

    @app.route("/actors", methods=["GET"])
    @requires_auth("get:actors")
    def get_actors(jwt):
        try:
            actors_bulk = Actor.query.order_by(Actor.id).all()
            if len(actors_bulk) == 0:
                abort(404)
            actors_formatted = [actor.format() for actor in actors_bulk]
            return (
                jsonify(
                    {
                        "success": True,
                        "actors": actors_formatted,
                        "total_actors": len(actors_formatted),
                    }
                ),
                200,
            )
        except ValueError:
            # Handle specific error for invalid data types
            abort(404)

    """
    Endpoint to handle GET requests
    for a specific movie.
    """

    @app.route("/movies/<int:movie_id>", methods=["GET"])
    @requires_auth("get:movie")
    def get_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            return jsonify({"success": True, "movie": movie.format()})
        except ValueError:
            # Handle specific error for invalid data types
            abort(404)

    """
    Endpoint to handle GET requests
    for a specific actor.
    """

    @app.route("/actors/<int:actor_id>", methods=["GET"])
    @requires_auth("get:actor")
    def get_actor(jwt, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            return jsonify({"success": True, "actor": actor.format()})
        except ValueError:
            # Handle specific error for invalid data types
            abort(404)

    """
    Endpoint to handle DELETE requests
    for a specific movie.
    """

    @app.route("/movies/<int:movie_id>", methods=["DELETE"])
    @requires_auth("delete:movie")
    def delete_movie(jwt, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()

            # Reset the sequence for the actors_id_seq
            max_id = db.session.query(db.func.max(Movie.id)).scalar()
            if max_id is not None:
                # Set the sequence to the next value
                db.session.execute(
                    text(f"SELECT setval('public.movies_id_seq', {max_id});")
                )
                db.session.commit()

            current_movies_bulk = Movie.query.order_by(Movie.id).all()
            current_movies = [movie.format() for movie in current_movies_bulk]
            return jsonify(
                {
                    "success": True,
                    "deleted": movie_id,
                    "current_movies": current_movies,
                    "total_movies": len(current_movies),
                }
            )
        except ValueError:
            # Handle specific error for invalid data types
            abort(404)

    """
    Endpoint to handle DELETE requests
    for a specific actor.
    """

    @app.route("/actors/<int:actor_id>", methods=["DELETE"])
    @requires_auth("delete:actor")
    def delete_actor(jwt, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()

            # Reset the sequence for the actors_id_seq
            max_id = db.session.query(db.func.max(Actor.id)).scalar()
            if max_id is not None:
                # Set the sequence to the next value
                db.session.execute(
                    text(f"SELECT setval('public.actors_id_seq', {max_id});")
                )
                db.session.commit()

            current_actors_bulk = Actor.query.order_by(Actor.id).all()
            current_actors = [actor.format() for actor in current_actors_bulk]
            return jsonify(
                {
                    "success": True,
                    "deleted": actor_id,
                    "current_actors": current_actors,
                    "total_actors": len(current_actors),
                }
            )
        except ValueError:
            # Handle specific error for invalid data types
            abort(404)

    """
    Endpoint to handle POST requests
    for a specific movie.
    """

    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movie")
    def create_movies(jwt):
        body = request.get_json()
        try:
            new_title = body.get("title")
            new_release_date = body.get("release_date")
            if not new_title or not new_release_date:
                abort(422)
            movie = Movie(title=new_title, release_date=new_release_date)
            max_id_movies = db.session.query(db.func.max(Movie.id)).scalar()
            if max_id_movies is not None:
                # Set the sequence to the next value
                db.session.execute(
                    text(f"SELECT setval('public.movies_id_seq', {max_id_movies});")
                )
            movie.insert()
            current_movies_bulk = Movie.query.order_by(Movie.id).all()
            current_movies = [movie.format() for movie in current_movies_bulk]
            return jsonify(
                {
                    "success": True,
                    "created": movie.id,
                    "movies": current_movies,
                    "total_movies": len(current_movies),
                }
            )
        except:
            abort(422)

    """
    Endpoint to handle POST requests
    for a specific actor.
    """

    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actor")
    def create_actors(jwt):
        body = request.get_json()
        try:
            new_name = body.get("name")
            new_age = body.get("age")
            new_gender = body.get("gender")
            if not new_name or not new_age or not new_gender:
                abort(422)
            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            max_id_actors = db.session.query(db.func.max(Actor.id)).scalar()
            if max_id_actors is not None:
                # Set the sequence to the next value
                db.session.execute(
                    text(f"SELECT setval('public.actors_id_seq', {max_id_actors});")
                )
            actor.insert()
            current_actors_bulk = Actor.query.order_by(Actor.id).all()
            current_actors = [actor.format() for actor in current_actors_bulk]
            return jsonify(
                {
                    "success": True,
                    "created": actor.id,
                    "actors": current_actors,
                    "total_actors": len(current_actors),
                }
            )
        except:
            abort(422)

    """
    Endpoint to handle PATCH requests
    for a specific movie.
    """

    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth("patch:movie")
    def update_movie(jwt, id):
        body = request.get_json()
        try:
            movie_to_patch = Movie.query.filter(Movie.id == id).one_or_none()
            if movie_to_patch is None:
                abort(422)
            title = body.get("title")
            release_date = body.get("release_date")

            # update the field if data is available
            if title:
                movie_to_patch.title = title
            if release_date:
                movie_to_patch.release_date = release_date
            if title is None and release_date is None:
                abort(422)

            movie_to_patch.update()

            return (
                jsonify({"success": True, "movie_patched": [movie_to_patch.format()]}),
                200,
            )
        except Exception as e:
            abort(422)

    """
    Endpoint to handle PATCH requests
    for a specific actor.
    """

    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth("patch:actor")
    def update_actor(jwt, id):
        body = request.get_json()
        try:
            actor_to_patch = Actor.query.filter(Actor.id == id).one_or_none()
            if actor_to_patch is None:
                abort(404)
            name = body.get("name")
            age = body.get("age")
            gender = body.get("gender")

            # update the field if data is available
            if name:
                actor_to_patch.name = name
            if age:
                actor_to_patch.age = age
            if gender:
                actor_to_patch.gender = gender
            if name is None and age is None and gender is None:
                abort(422)

            actor_to_patch.update()

            return (
                jsonify({"success": True, "actor_patched": [actor_to_patch.format()]}),
                200,
            )
        except Exception as e:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "internal server error"}
            ),
            500,
        )

    @app.errorhandler(AuthError)
    def handle_auth_error(error):
        response = {"error": error.error["code"], "message": error.error["description"]}
        return jsonify(response), error.status_code

    return app


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

database_path_app = DATABASE_URL_PRODUCTION
app = create_app(database_path_app)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
