# Capstone project

## Introduction

This project is the last one of the Full Stack Nanodegree of Udacity. 

Main work topics in this project:

1. Authorization using Auth0, using RBAC roles and jwt.
2. Coding standart compliant PEP8 using black.
3. Testing: all the endpoints were tested for good and bad weather using RBAC and error handling.
4. The required setup information was provided.
5. All the endpoints were properly documented.
6. Database management using psql and database migrations.
7. Deployment of the application into the cloud, using Heroku as a Cloud platform.

The theme of this project is a Casting Agency.
The Casting Agency models a company that is responsible  
of creating movies and 
managing and assigning actors to those movies. 

## Project setup

#### Python

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.


#### Run the application

To run the application first we have create and assign the environmental variables referring to the JWT token of the different roles (casting assistant, casting director and executive director) and the URI of the testing and production databases.

```bash
source setup.sh
```

The application at this point is ready to be deployed, allowing the testing of the different endpoints.

```bash
python app.py
```

The link of the application is the following

[https://capstone-project-photon-25f79f0bc990.herokuapp.com/](https://capstone-project-photon-25f79f0bc990.herokuapp.com/) 

### List of permissions

1. **GET movies**: &nbsp;&nbsp;&nbsp;&nbsp;list the entire list of movies
2. **GET actors**: &nbsp;&nbsp;&nbsp;&nbsp;list the entire list of actors
3. **GET movie**: &nbsp;&nbsp;&nbsp;&nbsp;list the information of a given movie
4. **GET actor**: &nbsp;&nbsp;&nbsp;&nbsp;list the information of a given actor
5. **DELETE movie**: &nbsp;&nbsp;&nbsp;&nbsp;delete a given movie
6. **DELETE actor**: &nbsp;&nbsp;&nbsp;&nbsp;delete a given actor
7. **POST movie**: &nbsp;&nbsp;&nbsp;&nbsp;post a new movie
8. **POST actor**: &nbsp;&nbsp;&nbsp;&nbsp;post a new actor
9. **PATCH movie**: &nbsp;&nbsp;&nbsp;&nbsp;patch an existing movie
10. **PATCH actor**: &nbsp;&nbsp;&nbsp;&nbsp;patch an existing actor

### List of Roles

1. **Casting Assistante**:
```javascript
    "permissions": [
                "get:actor",
                "get:actors",
                "get:movie",
                "get:movies"
            ] 
```
2. **Casting Director**: 
```javascript
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
```
3. **Executive Director**:

```javascript
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
```

### How to renew the jwt tokens in case of expiration

If the jwt tokens have expired, we can retrieve new ones by login in at an anonymous window, here are the several credentials for the different roles in this application:

1. **Casting assistant role**:
>- **email**: casting_assistant@gmail.com
>- **password**: Udacity123!

2. **Casting director role**:
>- **email**: casting_assistant@gmail.com
>- **password**: Udacity123!

3. **Executive director role**:
>- **email**: executive_director@gmail.com
>- **password**: Udacity123!

In case the token have expired then just perform a login with one of the credentials provided and extract the token from the URL that you will be redirected, here is an example:

```bash
https://capstone-project-photon-25f79f0bc990.herokuapp.com//success#access_token=<jwt_token>&expires_in=86400&token_type=Bearer
```

The tokens can then be copied to the file ```setup.sh``` and sourced, so that when running the tests, the endpoints have the right permissions.


### Run the testing

In terms of testing of the application, good and bad weather scenarios were tested for each endpoint, also for each RBAC for each role 2 tests were created.

To run the tests:
```bash
python test_capstone.py
```

### Error handling

There can be several type of errors got when using this API.

**Error code 400**

Example json error response:

```javascript
{
    "error": 400,
    "message": "bad request",
    "success": false
}
```

**Error code 404**

Example json error response:

```javascript
{
    "error": 404,
    "message": "resource not found",
    "success": false
}
```

**Error code 422**

Example json error response:

```javascript
{
    "error": 422,
    "message": "unprocessable",
    "success": false
}
```

**Error code 500**

Example json error response:

```javascript
{
    "error": 500,
    "message": "internal server error",
    "success": false
}
```

### Endpoints documentation

- [/](#root_endpoint)
- [success](#Success_endpoint)
- [GET movies](#GET_movies)
- [GET actors](#GET_actors)
- [GET movie](#GET_movie)
- [GET actor](#GET_actor)
- [DELETE movie](#DELETE_movie)
- [DELETE actor](#DELETE_actor)
- [POST movie](#POST_movie)
- [POST actor](#POST_actor)
- [PATCH movie](#PATCH_movie)
- [PATCH actor](#PATCH_actor)

---

<h4 id="Root_endpoint"></h4>

#### Root endpoint: '/'

This endpoint is the starting point of the application, from here the user can make the login and get a valid jwt token.

**Request arguments:**

- _None_

---

<h4 id="Success_endpoint"></h4>

#### Login success endpoint: '/success'

This serves as a confirmation that the login has been sucessfull, displaying a 'Login successfull to the browser' after the user has been logged in.

**Request arguments:** 

- _None_

**Returns:**

```javascript
{
    "Login successful"
}
```

---

<h4 id="GET_movies"></h4>

#### GET movies endpoint: '/movies'

This endpoint will return the full list of movies from the database.

**Request arguments:** 

- _None_

**Returns:**

```javascript
{
    "success": True,
    "movies": list_movies,
    "total_movies": total_movies
}
```

---

<h4 id="GET_actors"></h4>

#### GET actors endpoint: '/actors'

This endpoint will return the full list of actors from the database.

**Request arguments:** 

- _None_

**Returns:**

```javascript
{
    "success": True,
    "actors": list_actors,
    "total_movies": total_actors
}
```

---

<h4 id="GET_movie"></h4>

#### GET movie endpoint: '/movies/<int:movie_id>'

This endpoint will return the data from the movie with the id equal to movie_id from the database.

**Request arguments:** 

- _movie_id_ (Integer) of the movie to retrieve information

**Returns:**

```javascript
{
    "success": True,
    "movie": movie_data
}
```

---

<h4 id="GET_actor"></h4>

#### GET actor endpoint: '/actors/<int:actor_id>'

This endpoint will return the data from the actor with the id equal to actor_id from the database.

**Request arguments:** 

- _actor_id_ (Integer) of the actor to retrieve information

**Returns:**

```javascript
{
    "success": True,
    "actor": actor_data
}
```

---

<h4 id="DELETE_movie"></h4>

#### DELETE movie endpoint: '/movies/<int:movie_id>'

This endpoint will delete the movie with the movie_id from the database.

**Request arguments:** 

- _movie_id_ (Integer) of the movie to delete

**Returns:**

```javascript
{
    "success": True,
    "deleted": movie_id,
    "current_movies": current_list_movies,
    "total_movies": current_total_movies
}
```

---

<h4 id="DELETE_actor"></h4>

#### DELETE actor endpoint: '/actors/<int:actor_id>'

This endpoint will delete the actor with the actor_id from the database.

**Request arguments:** 

- _actor_id_ (Integer) of the actor to delete

**Returns:**

```javascript
{
    "success": True,
    "deleted": movie_id,
    "current_actors": current_list_actors,
    "total_actors": current_total_actors
}
```

---

<h4 id="POST_movie"></h4>

#### POST movie endpoint: '/movies'

This endpoint will create a new movie and insert into the database.

**Request arguments:** 

- _title_ (String) of the movie
- _release_date_ (Date) of the movie in the cinemas

**Returns:**

```javascript
{
    "success": True,
    "created": new_movie_id,
    "movies": new_movies_list,
    "total_movies": new_movies_total
}
```

---

<h4 id="POST_actor"></h4>

#### POST actor endpoint: '/actors'

This endpoint will create a new actor and insert into the database.

**Request arguments:** 

- _name_ (String) of the actor
- _age_ (Integer) of the actor
- _gender_ (String) of the actor

**Returns:**

```javascript
{
    "success": True,
    "created": new_actor_id,
    "actors": new_actors_list,
    "total_actors": new_actors_total
}
```

---

<h4 id="PATCH_movie"></h4>

#### PATCH movie endpoint: '/movies<int:id>'

This endpoint will patch an existing movie

**Request arguments:** 


- _id_ (Integer) of the movie

And at least one of this two arguments:
- _title_ (String) of the movie
- _release_date_ (Date) of the movie in the cinemas

**Returns:**

```javascript
{
    "success": True,
    "movie_patched": movie_patched_info
}
```

---

<h4 id="PATCH_actor"></h4>

#### PATCH actor endpoint: '/actors<int:id>'

This endpoint will patch an existing actor

**Request arguments:** 


- _id_ (Integer) of the actor

And at least one of this three arguments:
- _name_ (String) of the actor
- _age_ (Integer) of the actor
- _gender_ (String) of the actor

**Returns:**

```javascript
{
    "success": True,
    "actor_patched": actor_patched_info
}
```

