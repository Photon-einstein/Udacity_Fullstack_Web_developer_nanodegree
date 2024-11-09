# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account                          (DONE)
2. Select a unique tenant domain                       (DONE)
3. Create a new, single page web application           (DONE)
4. Create a new API                                    (DONE)
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:drinks`                                      (DONE)
   - `get:drinks-detail`                               (DONE)
   - `post:drinks`                                     (DONE)
   - `patch:drinks`                                    (DONE)
   - `delete:drinks`                                   (DONE)
6. Create new roles for:
   - Barista
     - can `get:drinks-detail`                         (DONE)
     - can `get:drinks`                                (DONE)
   - Manager
     - can perform all actions                         (DONE)
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Barista role to one and Manager role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
   - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`


Barista jwt: (Test done) (pass: B*******!)
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5CZ0J3X2VUckFBeDRRQ2FfV3JITiJ9.eyJpc3MiOiJodHRwczovL2Rldi1uOHpsdjJodjhkaWZqbXp4LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzJlYTBkMjc3N2EwMzMwYTljMGE2M2IiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjgxMDAvZ2V0LWRyaW5rcyIsImlhdCI6MTczMTEwOTI1NywiZXhwIjoxNzMxMTE2NDU3LCJzY29wZSI6IiIsImF6cCI6Img3RmtKcEZqMm9hbmtsd3Z0WXBibmhXT3N4QlR2TWNaIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIl19.Q-UHjfhAlg5sFNAsA3FA-XYkEKrdWu-1ieDHVU2EwrXEInBOlFUSJHjSPo-YLsDuoeiZdqw8aiMEEOZUnRzmQKgbGpvOsOrMR11Opr9vyuf69J_P0tREyH1NVJcFDDVuk9l1zUN_3LWM3bQEHLVTVwdt-LIt3y-lWRaUuM1i3EQ-0sad8P8qzBkQZ0YcWtk9HjWUAeESioaxUykWbrgcfj48nKrnuLkXIB79Veh_Z44r4GpiqFX20jOPZwoDUYzudkLVTJ1kfyybZw56CaAC0--wz22e8XzRY7inBj5H0tS6hgo2F9wKyynHsWDSaYlkLQCSmXy0fmJ0VLNWO4yKpg

Manager jwt: (Test DONE)
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5CZ0J3X2VUckFBeDRRQ2FfV3JITiJ9.eyJpc3MiOiJodHRwczovL2Rldi1uOHpsdjJodjhkaWZqbXp4LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NzJlYTgyOTMzODIxMDUyMjQyZDI4YzMiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjgxMDAvZ2V0LWRyaW5rcyIsImlhdCI6MTczMTExMTAxNiwiZXhwIjoxNzMxMTE4MjE2LCJzY29wZSI6IiIsImF6cCI6Img3RmtKcEZqMm9hbmtsd3Z0WXBibmhXT3N4QlR2TWNaIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.nQMnB6qdESlAfmx7Zox6Tqxua7KPwvawEO0-rWCcYhmHhJaOpJjBB_8g4C8hKNKwxKtxRORdWYW_AvoH8gWG6U1FqvPXj6DRJsN7IAI2judcbcVa6lW1MhhDhfGN0_CDoOPElswdmJ5hRCAG_vYU80_qjbdaSg9PctW9Ein25cmZYKf_ZIAV8NphFPYrvOgCGHt3m297vz3yLKrh3PcYh2TdFcalb0DaA-epjAPwglUidmGEGL_8nst2_AGdrjZtoYzDXjQAcYUKPQeC7meMezDXaw9DIk2_8ctIjPh3kXc9RrD-Dh5SrXLfcpLhqT_E9hHAq7AgOWXIEljf7gLIUg